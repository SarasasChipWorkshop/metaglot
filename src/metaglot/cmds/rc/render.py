import logging

from ...cli import RcRenderOpts
from ...filters import register_general_filters, register_rc_filters
from ...langid import PoLang, WinLcid
from ...langmap import win_lcid_map
from ...manifest import Manifest, load_manifest
from ...pofile import LanguagePack, resolve_glob_files, resolve_translations
from ...render import create_environment, render

_CODE_PAGE = 1200
"""The Unicode (UTF-16) code page used by VERSIONINFO resources.

MetaGlot reads and writes everything as UTF-8, so this code page is a fixed
constraint of the pipeline, not a configuration point.
"""


def _lookup_langid(lang: PoLang) -> WinLcid:
    try:
        return win_lcid_map.lookup(lang)
    except KeyError:
        raise ValueError(f"language '{lang}' has no Windows language mapping") from None


def _language_context(pack: LanguagePack, manifest: Manifest) -> dict:
    lcid = _lookup_langid(pack.lang)
    return {
        "name": pack.lang.value,
        "langid": f"0x{lcid.value:04X}",
        "primary": f"0x{lcid.primary:02X}",
        "sublanguage": f"0x{lcid.sublanguage:02X}",
        "block_key": f"{lcid.value:04X}{_CODE_PAGE:04X}",
        "code_page": f"{_CODE_PAGE}",
        "strings": pack.translations,
    }


def run(opts: RcRenderOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    packs = resolve_translations(manifest, resolve_glob_files(opts.in_po))
    languages = [_language_context(pack, manifest) for pack in packs.values()]
    logging.info(
        "rendering languages: %s",
        ", ".join(language["name"] for language in languages),
    )
    env = create_environment()
    register_general_filters(env)
    register_rc_filters(env)
    render(env, opts.in_template, {"languages": languages}, opts.out_rc)
