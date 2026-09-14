import logging
from pathlib import Path

from liquid import Environment, StrictUndefined
from liquid.exceptions import LiquidError

from . import winlang
from .catalog import collect_po_files, load_po
from .manifest import Manifest, load_manifest


def _rc_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _create_environment() -> Environment:
    env = Environment(undefined=StrictUndefined)
    env.add_filter("rc_escape", _rc_escape)
    return env


def _language_context(
    locale: str,
    language: winlang.WindowsLanguage,
    translations: dict[str, str],
    manifest: Manifest,
) -> dict:
    entries = manifest.entries
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
                "text": translations.get(entry.msgid, entry.msgid),
                "context": entry.context,
            }
            for key, entry in entries
        ],
        "named": {
            key: translations.get(entry.msgid, entry.msgid)
            for key, entry in entries
        },
    }


def render(manifest_path: Path, po_patterns: list[Path], template_path: Path, output_path: Path) -> None:
    manifest = load_manifest(manifest_path)
    known = manifest.msgids

    collected = []
    locale_sources: dict[str, Path] = {}
    for po_path in collect_po_files(po_patterns):
        locale, translations = load_po(po_path)
        unknown = sorted(set(translations) - known)
        if unknown:
            raise ValueError(
                f"{po_path.name} contains unknown msgid(s): {', '.join(unknown)}"
            )
        if locale in locale_sources:
            raise ValueError(
                f"duplicate locale '{locale}' found in '{locale_sources[locale].name}' and '{po_path.name}'"
            )
        locale_sources[locale] = po_path
        try:
            language = winlang.lookup(locale)
        except KeyError:
            raise ValueError(
                f"locale '{locale}' (from {po_path.name}) has no Windows language mapping"
            ) from None
        collected.append((locale, language, translations))

    english = winlang.lookup("en")
    english_po = next(
        (item for item in collected if item[1].langid == english.langid), None
    )
    others = sorted(
        (item for item in collected if item[1].langid != english.langid),
        key=lambda item: item[1].langid,
    )
    ordered = [
        ("en", english, english_po[2] if english_po else {}),
        *others,
    ]

    languages = [
        _language_context(locale, language, translations, manifest)
        for locale, language, translations in ordered
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
