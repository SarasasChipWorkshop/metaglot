import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ...filters import register_general_filters, register_rc_filters
from ...langid import PoLang, WinLcid
from ...langmap import win_lcid_map
from ...manifest import Manifest, load_manifest
from ...pofile import (
    LanguagePack,
    build_default_pack,
    resolve_glob_files,
    resolve_translations,
)
from ...render import create_environment, render

_CODE_PAGE = 1200
"""The Unicode (UTF-16) code page used by VERSIONINFO resources.

MetaGlot reads and writes everything as UTF-8, so this code page is a fixed
constraint of the pipeline, not a configuration point.
"""

_MANIFEST_DEST = "manifest"
_PO_DEST = "po"
_TEMPLATE_DEST = "template"
_OUTPUT_DEST = "output"


@dataclass(frozen=True)
class RcRenderOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    in_po: list[Path]
    """The path to input PO files to read, each may be a glob pattern."""
    in_template: Path
    """The path to the input user-provided Liquid for rendering."""
    out_rc: Path
    """The path of the output rendered Windows RC file."""


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
        help="The path of the output rendered Windows RC file.",
        metavar="FILE",
    )


def parse(args: dict[str, Any]) -> RcRenderOpts:
    return RcRenderOpts(
        args[_MANIFEST_DEST],
        args[_PO_DEST],
        args[_TEMPLATE_DEST],
        args[_OUTPUT_DEST],
    )


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
    # The manifest's source language is always rendered: taken from a PO file
    # when available, synthesized from the source strings otherwise.
    if manifest.source_language not in packs:
        packs[manifest.source_language] = build_default_pack(
            manifest, manifest.source_language
        )
    languages = [_language_context(pack, manifest) for pack in packs.values()]
    logging.info(
        "rendering languages: %s",
        ", ".join(language["name"] for language in languages),
    )
    env = create_environment()
    register_general_filters(env)
    register_rc_filters(env)
    render(env, opts.in_template, {"languages": languages}, opts.out_rc)
