import glob
import logging
from pathlib import Path

import polib

from .manifest import Manifest, load_manifest

_POT_HEADER = {
    "Project-Id-Version": "PACKAGE VERSION",
    "PO-Revision-Date": "YEAR-MO-DA HO:MI+ZONE",
    "Last-Translator": "FULL NAME <EMAIL@ADDRESS>",
    "Language-Team": "LANGUAGE <LL@li.org>",
    "MIME-Version": "1.0",
    "Content-Type": "text/plain; charset=UTF-8",
    "Content-Transfer-Encoding": "8bit",
}


def collect_po_files(patterns: list[Path]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        matched = sorted(glob.glob(str(pattern)))
        if not matched:
            raise ValueError(f"the pattern '{pattern}' matched no PO file")
        for name in matched:
            file = Path(name)
            resolved = file.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(file)
    return files


def load_po(path: Path) -> tuple[str, dict[str, str]]:
    try:
        po = polib.pofile(str(path))
    except (OSError, IOError) as exc:
        raise RuntimeError(f"failed to read PO file '{path}': {exc}") from exc
    locale = po.metadata.get("Language") or path.stem
    translations = {
        entry.msgid: entry.msgstr
        for entry in po
        if entry.msgstr and "fuzzy" not in entry.flags
    }
    return locale, translations


def generate(manifest_path: Path, output_path: Path) -> None:
    manifest: Manifest = load_manifest(manifest_path)
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
    output_path.parent.mkdir(parents=True, exist_ok=True)
    po.save(str(output_path))
    logging.info("wrote %d entries to %s", len(po), output_path)
