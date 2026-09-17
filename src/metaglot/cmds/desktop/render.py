import logging

from ...cli import DesktopRenderOpts
from ...filters import register_desktop_filters, register_general_filters
from ...langmap import desktop_lang_map
from ...manifest import Manifest, load_manifest
from ...pofile import (
    LanguagePack,
    build_default_pack,
    resolve_glob_files,
    resolve_translations,
)
from ...render import create_environment, render


def _language_context(pack: LanguagePack, manifest: Manifest) -> dict:
    locale = desktop_lang_map.convert(pack.lang)
    return {
        "name": pack.lang.value,
        "locale": locale.value,
        "strings": pack.translations,
    }


def run(opts: DesktopRenderOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    packs = resolve_translations(manifest, resolve_glob_files(opts.in_po))
    default = _language_context(
        build_default_pack(manifest, manifest.source_language), manifest
    )
    entries = [_language_context(pack, manifest) for pack in packs.values()]
    logging.info(
        "rendering languages: %s (default %s)",
        ", ".join(entry["name"] for entry in entries),
        default["name"],
    )
    env = create_environment()
    register_general_filters(env)
    register_desktop_filters(env)
    render(
        env, opts.in_template, {"languages": entries, "default": default},
        opts.out_desktop,
    )
