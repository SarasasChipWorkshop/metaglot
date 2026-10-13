import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ...filters import register_appstream_filters, register_general_filters
from ...langid import AppStreamLang, PoLang
from ...langmap import appstream_lang_map
from ...manifest import load_manifest
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


class _AppStreamStringsView:
    """Route template string key lookups to their resolved text."""

    __pack: LanguagePack
    """The language pack the lookups route to."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack

    def __getitem__(self, key: str) -> str:
        return self.__pack.translations[key].text


class _AppStreamLanguageView:
    """The Liquid-facing view of one language for AppStream rendering."""

    __pack: LanguagePack
    """The wrapped language pack."""
    __strings: _AppStreamStringsView
    """The view of the pack's translations."""
    __lang: AppStreamLang
    """The BCP 47 language tag of the pack's language."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack
        self.__strings = _AppStreamStringsView(pack)
        self.__lang = appstream_lang_map.convert(pack.lang)

    def __getitem__(self, key: str) -> object:
        match key:
            case "name":
                return self.__pack.lang.value
            case "strings":
                return self.__strings
            case "lang":
                return self.__lang.value
            case _:
                raise KeyError(key)


class _AppStreamRenderContext:
    """The Liquid-facing top-level context for AppStream rendering."""

    __languages: tuple[_AppStreamLanguageView, ...]
    """The views of every translation language."""
    __default: _AppStreamLanguageView
    """The view of the manifest's source language."""

    def __init__(self, packs: dict[PoLang, LanguagePack], default: LanguagePack):
        self.__languages = tuple(
            _AppStreamLanguageView(pack) for pack in packs.values()
        )
        self.__default = _AppStreamLanguageView(default)

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ("languages", "default")

    def __getitem__(self, key: str) -> object:
        match key:
            case "languages":
                return self.__languages
            case "default":
                return self.__default
            case _:
                raise KeyError(key)


def run(opts: AppStreamRenderOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    packs = resolve_translations(manifest, resolve_glob_files(opts.in_po))
    default = build_default_pack(manifest, manifest.source_language)
    context = _AppStreamRenderContext(packs, default)
    logging.info(
        "Rendering FreeDesktop AppStream file with languages: %s (default %s)",
        ", ".join(str(pack.lang) for pack in packs.values()),
        default.lang,
    )
    env = create_environment()
    register_general_filters(env)
    register_appstream_filters(env)
    render(env, opts.in_template, context, opts.out_appstream)
