import logging
from pathlib import Path

from liquid import Environment, StrictUndefined
from liquid.exceptions import LiquidError

from . import winlang
from .langid import PoLang
from .manifest import Manifest, load_manifest
from .pofile import LanguagePack, resolve_glob_files, resolve_translations


def _rc_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _create_environment() -> Environment:
    env = Environment(undefined=StrictUndefined)
    env.add_filter("rc_escape", _rc_escape)
    return env


def _language_context(
    locale: str,
    language: winlang.WindowsLanguage,
    pack: LanguagePack,
    manifest: Manifest,
) -> dict:
    return {
        "name": language.name,
        "locale": locale,
        "langid": f"0x{language.langid:X}",
        "primary": f"0x{language.primary:02X}",
        "sublanguage": f"0x{language.sublanguage:02X}",
        "block_key": f"{language.langid:04X}04B0",
        "strings": [
            {
                "key": key,
                "msgid": entry.msgid,
                "text": pack.translations[key],
                "context": entry.context,
            }
            for key, entry in manifest.strings.items()
        ],
        "named": pack.translations,
    }


def _lookup_windows_language(lang: PoLang) -> winlang.WindowsLanguage:
    try:
        return winlang.lookup(lang.value)
    except KeyError:
        raise ValueError(
            f"language '{lang}' has no Windows language mapping"
        ) from None


def render(
    manifest_path: Path,
    po_patterns: list[Path],
    template_path: Path,
    output_path: Path,
) -> None:
    manifest = load_manifest(manifest_path)
    packs = resolve_translations(manifest, resolve_glob_files(po_patterns))

    english = winlang.lookup("en")
    resolved = [(pack, _lookup_windows_language(pack.lang)) for pack in packs.values()]
    english_item = next(
        (item for item in resolved if item[1].langid == english.langid), None
    )
    others = [item for item in resolved if item[1].langid != english.langid]
    if english_item is None:
        english_pack = LanguagePack(
            PoLang("en"),
            {key: entry.msgid for key, entry in manifest.strings.items()},
        )
        ordered = [(english_pack, english), *others]
    else:
        ordered = [english_item, *others]

    languages = [
        _language_context(pack.lang.value, language, pack, manifest)
        for pack, language in ordered
    ]

    if not template_path.is_file():
        raise ValueError(f"template file not found: {template_path}")
    try:
        template_source = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to read template '{template_path}': {exc}") from exc

    env = _create_environment()
    try:
        template = env.from_string(
            template_source, name=str(template_path), path=template_path
        )
        content = template.render(languages=languages)
    except LiquidError as exc:
        raise RuntimeError(
            f"failed to render template '{template_path}': {exc}"
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8", newline="\n")
    logging.info(
        "wrote %s with languages: %s",
        output_path,
        ", ".join(language["name"] for language in languages),
    )
