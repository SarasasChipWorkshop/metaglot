import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ...filters import (
    register_general_filters,
    register_plist_info_filters,
    register_plist_strings_filters,
)
from ...langmap import plist_lang_map
from ...manifest import load_manifest
from ...pofile import (
    LanguagePack,
    build_default_pack,
    resolve_glob_files,
    resolve_translations,
)
from ...render import create_environment, render, render_path

_PLIST_DEST = "plist"
_PO_DEST = "po"
_PLIST_TEMPLATE_DEST = "plist_template"
_STRINGS_TEMPLATE_DEST = "strings_template"
_PLIST_PATH_DEST = "plist_path"
_STRINGS_PATH_DEST = "strings_path"
_OUTPUT_DEST = "output"


@dataclass(frozen=True)
class PlistRenderOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    in_po: list[Path]
    """The path to input PO files to read, each may be a glob pattern."""
    in_plist_template: Path
    """The path to the input user-provided Liquid for the Info.plist file."""
    in_strings_template: Path
    """The path to the input user-provided Liquid for the InfoPlist.strings files."""
    in_plist_path: str
    """The Liquid template resolving the output path of the Info.plist file."""
    in_strings_path: str
    """The Liquid template resolving the output path of every InfoPlist.strings file."""
    out_dir: Path
    """The path of the output folder holding every rendered file."""


def register(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--manifest",
        dest=_PLIST_DEST,
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
        "--plist-template",
        dest=_PLIST_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input user-provided Liquid for the Info.plist file.",
        metavar="FILE",
    )
    parser.add_argument(
        "--strings-template",
        dest=_STRINGS_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help=(
            "The path to the input user-provided Liquid for the "
            "InfoPlist.strings files."
        ),
        metavar="FILE",
    )
    parser.add_argument(
        "--plist-path",
        dest=_PLIST_PATH_DEST,
        action="store",
        type=str,
        required=True,
        help=(
            "The Liquid template resolving the output path of the Info.plist "
            "file, relative to the output folder."
        ),
        metavar="TEMPLATE",
    )
    parser.add_argument(
        "--strings-path",
        dest=_STRINGS_PATH_DEST,
        action="store",
        type=str,
        required=True,
        help=(
            "The Liquid template resolving the output path of every "
            "InfoPlist.strings file, relative to the output folder. It is "
            "rendered once per language with the language tag exposed "
            "as 'lang'."
        ),
        metavar="TEMPLATE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest=_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path of the output folder holding every rendered file.",
        metavar="DIR",
    )


def parse(args: dict[str, Any]) -> PlistRenderOpts:
    return PlistRenderOpts(
        args[_PLIST_DEST],
        args[_PO_DEST],
        args[_PLIST_TEMPLATE_DEST],
        args[_STRINGS_TEMPLATE_DEST],
        args[_PLIST_PATH_DEST],
        args[_STRINGS_PATH_DEST],
        args[_OUTPUT_DEST],
    )


class _PlistStringsView:
    """Route template string key lookups to their resolved text."""

    __pack: LanguagePack
    """The language pack the lookups route to."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack

    def __getitem__(self, key: str) -> str:
        return self.__pack.translations[key].text


class _PlistSourcesView:
    """Route template string key lookups to their manifest source text."""

    __pack: LanguagePack
    """The language pack the lookups route to."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack

    def __getitem__(self, key: str) -> str:
        return self.__pack.translations[key].entry.msgid


class _PlistInfoPathContext:
    """The Liquid-facing context of the Info.plist path template.

    The context is empty: the Info.plist path is typically the plain
    literal 'Contents/Info.plist', and referencing any variable fails
    the render.
    """

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ()

    def __getitem__(self, key: str) -> object:
        raise KeyError(key)


class _PlistStringsPathContext:
    """The Liquid-facing context of one InfoPlist.strings path template
    rendering.

    It is rendered once per language, with the language tag of the
    InfoPlist.strings file being placed exposed as ``lang``.
    """

    __lang: str
    """The BCP 47 language tag of the InfoPlist.strings file being placed."""

    def __init__(self, lang: str):
        self.__lang = lang

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ("lang",)

    def __getitem__(self, key: str) -> object:
        if key == "lang":
            return self.__lang
        raise KeyError(key)


class _PlistStringsTemplateContext:
    """The Liquid-facing top-level context of every InfoPlist.strings
    file rendering.

    The members of the current language are exposed at the top level.
    The structure is identical for every language; only the data differs.
    The class also serves as the value of ``default`` inside the Info.plist
    template context, where it exposes the source language the same way.
    """

    __pack: LanguagePack
    """The wrapped language pack."""
    __strings: _PlistStringsView
    """The view of the pack's resolved translations."""
    __sources: _PlistSourcesView
    """The view of the pack's manifest source texts."""
    __lang: str
    """The BCP 47 language tag of the pack's language."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack
        self.__strings = _PlistStringsView(pack)
        self.__sources = _PlistSourcesView(pack)
        self.__lang = plist_lang_map.convert(pack.lang).value

    def keys(self) -> tuple[str, ...]:
        """Return the names of the exposed template variables."""
        return ("name", "lang", "strings", "sources")

    def __getitem__(self, key: str) -> object:
        match key:
            case "name":
                return self.__pack.lang.value
            case "lang":
                return self.__lang
            case "strings":
                return self.__strings
            case "sources":
                return self.__sources
            case _:
                raise KeyError(key)


class _PlistInfoTemplateContext:
    """The Liquid-facing top-level context of the Info.plist file rendering."""

    __default: _PlistStringsTemplateContext
    """The view of the manifest's source language."""
    __langs: tuple[str, ...]
    """The BCP 47 language tags of every language, source language first."""

    def __init__(self, source: LanguagePack, langs: tuple[str, ...]):
        self.__default = _PlistStringsTemplateContext(source)
        self.__langs = langs

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ("default", "langs")

    def __getitem__(self, key: str) -> object:
        match key:
            case "default":
                return self.__default
            case "langs":
                return self.__langs
            case _:
                raise KeyError(key)


def run(opts: PlistRenderOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    packs = resolve_translations(manifest, resolve_glob_files(opts.in_po))
    # The source language always leads the language list and always gets
    # an InfoPlist.strings file: its .lproj folder is the fallback
    # localization of the bundle.
    source = packs.pop(manifest.source_language, None)
    if source is None:
        source = build_default_pack(manifest, manifest.source_language)
    ordered = [source, *packs.values()]
    langs = tuple(plist_lang_map.convert(pack.lang).value for pack in ordered)
    logging.info("rendering languages: %s", ", ".join(langs))

    # Every component renders with its own environment, so their filters
    # never interfere with each other.
    plist_path_env = create_environment()
    register_general_filters(plist_path_env)
    strings_path_env = create_environment()
    register_general_filters(strings_path_env)
    plist_template_env = create_environment()
    register_general_filters(plist_template_env)
    register_plist_info_filters(plist_template_env)
    strings_template_env = create_environment()
    register_general_filters(strings_template_env)
    register_plist_strings_filters(strings_template_env)

    plist_out = opts.out_dir / render_path(
        plist_path_env, opts.in_plist_path, _PlistInfoPathContext()
    )
    plist_out.parent.mkdir(parents=True, exist_ok=True)
    render(
        plist_template_env,
        opts.in_plist_template,
        _PlistInfoTemplateContext(source, langs),
        plist_out,
    )

    for pack, lang in zip(ordered, langs):
        strings_out = opts.out_dir / render_path(
            strings_path_env,
            opts.in_strings_path,
            _PlistStringsPathContext(lang),
        )
        strings_out.parent.mkdir(parents=True, exist_ok=True)
        render(
            strings_template_env,
            opts.in_strings_template,
            _PlistStringsTemplateContext(pack),
            strings_out,
        )
