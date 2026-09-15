import glob
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Optional
import polib
from .langid import PoLang
from .manifest import Manifest

_POT_HEADER = {
    "Project-Id-Version": "PACKAGE VERSION",
    "POT-Creation-Date": "YEAR-MO-DA HO:MI+ZONE",
    "PO-Revision-Date": "YEAR-MO-DA HO:MI+ZONE",
    "Last-Translator": "FULL NAME <EMAIL@ADDRESS>",
    "Language-Team": "LANGUAGE <LL@li.org>",
    "MIME-Version": "1.0",
    "Content-Type": "text/plain; charset=UTF-8",
    "Content-Transfer-Encoding": "8bit",
    "X-Generator": "MetaGlot/polib",
}


@dataclass(frozen=True)
class LanguagePack:
    """Resolved translations of one language against a manifest."""

    lang: PoLang
    """The language of this pack."""

    translations: dict[str, str]
    """The resolved text of every manifest entry, keyed by manifest entry key."""


def resolve_glob_files(patterns: Iterable[Path]) -> Iterator[Path]:
    """Lazily iterate the files matched by the given glob patterns.

    A pattern matching no file only produces a warning. A file matched by
    several patterns is yielded once per matching pattern.

    :param patterns: The glob patterns to match.
    :return: An iterator of resolved file paths.
    """
    for pattern in patterns:
        matched = tuple(Path(p) for p in glob.glob(str(pattern)))
        if len(matched) == 0:
            logging.warning("Pattern %s does not match any file.", pattern)
        for name in matched:
            yield name.resolve()


def resolve_translations(
    manifest: Manifest, po_paths: Iterable[Path]
) -> dict[PoLang, LanguagePack]:
    """Resolve the translations of the given PO files against a manifest.

    Each PO file is loaded lazily and resolved to a :class:`LanguagePack`
    holding the text of every manifest entry. Entries that are missing,
    untranslated or marked fuzzy fall back to their source string.

    :param manifest: The manifest describing all translatable entries.
    :param po_paths: The PO file paths to resolve.
    :return: A mapping from each language to its resolved language pack.
    :raises ValueError: If two PO files describe the same language, or a PO
        file contains entries unknown to the manifest.
    """
    # Collect every (msgid, context) pair the manifest defines. PO entries
    # matching none of them are rejected below.
    expected = {(entry.msgid, entry.context) for entry in manifest.strings.values()}
    # The resolved packs being built, keyed by language.
    packs: dict[PoLang, LanguagePack] = {}
    # Which file introduced each language, for duplicate reporting.
    sources: dict[PoLang, Path] = {}
    for path in po_paths:
        # Load the PO file and identify its language.
        po = _load_po(path)
        lang = _extract_lang(path, po)

        # One language must come from exactly one PO file.
        if lang in packs:
            raise ValueError(
                f"duplicate language '{lang}' found in "
                f"'{sources[lang].name}' and '{path.name}'"
            )
        sources[lang] = path

        # Index the entries by their (msgid, msgctxt) pair, so that lookups
        # and set operations share one pass over the file. Obsolete entries
        # are ignored, mirroring how polib's find() treats them.
        index: dict[tuple[str, Optional[str]], polib.POEntry] = {
            (entry.msgid, entry.msgctxt): entry for entry in po if not entry.obsolete
        }

        # Reject entries the manifest does not define.
        unknown = index.keys() - expected
        if unknown:
            rendered = ", ".join(
                f"{msgid!r}" if context is None else f"{msgid!r} (context {context!r})"
                for msgid, context in unknown
            )
            raise ValueError(
                f"'{path.name}' contains entry(s) unknown to the manifest: {rendered}"
            )

        # Resolve every manifest entry against the index. Entries that are
        # missing, untranslated or fuzzy fall back to their source string.
        translations = {
            key: _translated_text(index.get((entry.msgid, entry.context)), entry.msgid)
            for key, entry in manifest.strings.items()
        }
        packs[lang] = LanguagePack(lang, translations)
    return packs


def generate_pot(manifest: Manifest, output_path: Path) -> None:
    """Generate a POT template file from a manifest.

    :param manifest: The manifest holding the translatable strings.
    :param output_path: The path of the POT file to write.
    """
    po = polib.POFile()
    po.metadata = _POT_HEADER
    for _, entry in manifest.strings.items():
        po.append(
            polib.POEntry(
                msgid=entry.msgid,
                msgstr="",
                msgctxt=entry.context or None,
                comment=entry.comment or None,
            )
        )
    po.save(str(output_path))
    logging.info("Wrote %d entries to POT file '%s'.", len(po), output_path)


def _load_po(path: Path) -> polib.POFile:
    """Load and parse a PO file.

    :param path: The path of the PO file to load.
    :return: The parsed PO file.
    :raises RuntimeError: If the file cannot be read or parsed.
    """
    try:
        return polib.pofile(str(path))
    except OSError as exc:
        raise RuntimeError(f"failed to read PO file '{path}': {exc}") from exc


def _extract_lang(path: Path, po: polib.POFile) -> PoLang:
    """Extract the language of a loaded PO file.

    The ``Language`` metadata field is tried first, then the file name
    without extension.

    :param path: The path of the PO file, used for fallback and reporting.
    :param po: The loaded PO file.
    :return: The language of the PO file.
    :raises RuntimeError: If no valid language can be extracted.
    """
    metadata_language = po.metadata.get("Language")
    if metadata_language is not None:
        try:
            return PoLang(metadata_language)
        except ValueError:
            pass

    try:
        return PoLang(path.stem)
    except ValueError:
        pass

    raise RuntimeError(f"can't fetch valid language id in PO file '{path}'")


def _translated_text(entry: Optional[polib.POEntry], fallback: str) -> str:
    """Return the usable translation of an entry.

    :param entry: The PO entry to read, or ``None`` when absent.
    :param fallback: The source string used when the entry is missing,
        untranslated or marked fuzzy.
    :return: The usable translation.
    """
    if entry is None or entry.msgstr == "" or entry.fuzzy:
        return fallback
    return entry.msgstr
