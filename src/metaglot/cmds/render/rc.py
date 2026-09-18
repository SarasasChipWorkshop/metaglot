import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ...filters import register_general_filters, register_rc_filters
from ...langid import PoLang, WinLcid
from ...langmap import win_lcid_map
from ...manifest import load_manifest
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


class _RcStringsView:
    """Route template string key lookups to their resolved text."""

    __pack: LanguagePack
    """The language pack the lookups route to."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack

    def __getitem__(self, key: str) -> str:
        return self.__pack.translations[key].text


class _RcLanguageView:
    """The Liquid-facing view of one language for RC rendering."""

    __pack: LanguagePack
    """The wrapped language pack."""
    __strings: _RcStringsView
    """The view of the pack's translations."""
    __lcid: WinLcid
    """The Windows language identifier of the pack's language."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack
        self.__strings = _RcStringsView(pack)
        self.__lcid = _lookup_langid(pack.lang)

    def __getitem__(self, key: str) -> object:
        match key:
            case "name":
                return self.__pack.lang.value
            case "strings":
                return self.__strings
            case "langid":
                return f"0x{self.__lcid.value:04X}"
            case "primary":
                return f"0x{self.__lcid.primary:02X}"
            case "sublanguage":
                return f"0x{self.__lcid.sublanguage:02X}"
            case "block_key":
                return f"{self.__lcid.value:04X}{_CODE_PAGE:04X}"
            case "code_page":
                return f"{_CODE_PAGE}"
            case _:
                raise KeyError(key)


class _RcRenderContext:
    """The Liquid-facing top-level context for RC rendering."""

    __languages: tuple[_RcLanguageView, ...]
    """The views of every rendered language."""

    def __init__(self, packs: dict[PoLang, LanguagePack]):
        self.__languages = tuple(_RcLanguageView(pack) for pack in packs.values())

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ("languages",)

    def __getitem__(self, key: str) -> object:
        match key:
            case "languages":
                return self.__languages
            case _:
                raise KeyError(key)


def run(opts: RcRenderOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    packs = resolve_translations(manifest, resolve_glob_files(opts.in_po))
    # The manifest's source language is always rendered: taken from a PO file
    # when available, synthesized from the source strings otherwise.
    if manifest.source_language not in packs:
        packs[manifest.source_language] = build_default_pack(
            manifest, manifest.source_language
        )
    context = _RcRenderContext(packs)
    logging.info(
        "rendering languages: %s",
        ", ".join(str(pack.lang) for pack in packs.values()),
    )
    env = create_environment()
    register_general_filters(env)
    register_rc_filters(env)
    render(env, opts.in_template, context, opts.out_rc)
