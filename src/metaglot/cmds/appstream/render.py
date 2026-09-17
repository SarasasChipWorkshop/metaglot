import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ...filters import register_appstream_filters, register_general_filters
from ...langmap import appstream_lang_map
from ...manifest import Manifest, load_manifest
from ...pofile import (
    LanguagePack,
    build_default_pack,
    resolve_glob_files,
    resolve_translations,
)
from ...render import create_environment, render

_MANIFEST_DEST = "manifest"
_PO_DEST = "po"
_TEMPLATE_DEST = "template"
_OUTPUT_DEST = "output"


@dataclass(frozen=True)
class AppStreamRenderOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    in_po: list[Path]
    """The path to input PO files to read, each may be a glob pattern."""
    in_template: Path
    """The path to the input user-provided Liquid for rendering."""
    out_appstream: Path
    """The path of the output rendered AppStream XML file."""


def register(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--manifest",
        dest=_MANIFEST_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to input manifest file including translation strings.",
        metavar="FILE",
    )
    parser.add_argument(
        "-p",
        "--po",
        dest=_PO_DEST,
        action="extend",
        nargs="+",
        type=Path,
        required=True,
        help="The PO files to read, each may be a glob pattern.",
        metavar="GLOB",
    )
    parser.add_argument(
        "-t",
        "--template",
        dest=_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input user-provided Liquid for rendering.",
        metavar="FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest=_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path of the output rendered AppStream XML file.",
        metavar="FILE",
    )


def parse(args: dict[str, Any]) -> AppStreamRenderOpts:
    return AppStreamRenderOpts(
        args[_MANIFEST_DEST],
        args[_PO_DEST],
        args[_TEMPLATE_DEST],
        args[_OUTPUT_DEST],
    )


def _language_context(pack: LanguagePack, manifest: Manifest) -> dict:
    lang = appstream_lang_map.convert(pack.lang)
    return {
        "name": pack.lang.value,
        "lang": lang.value,
        "strings": pack.translations,
    }


def run(opts: AppStreamRenderOpts) -> None:
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
    register_appstream_filters(env)
    render(
        env, opts.in_template, {"languages": entries, "default": default},
        opts.out_appstream,
    )
