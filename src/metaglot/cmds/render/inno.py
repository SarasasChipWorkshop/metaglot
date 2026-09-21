import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ...filters import register_general_filters, register_inno_filters
from ...manifest import load_manifest
from ...pofile import (
    LanguagePack,
    build_default_pack,
    resolve_glob_files,
    resolve_translations,
)
from ...render import create_environment, render, render_path

_MANIFEST_DEST = "manifest"
_PO_DEST = "po"
_ISS_TEMPLATE_DEST = "iss_template"
_ISL_TEMPLATE_DEST = "isl_template"
_ISS_PATH_DEST = "iss_path"
_ISL_PATH_DEST = "isl_path"
_OUTPUT_DEST = "output"


@dataclass(frozen=True)
class InnoRenderOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    in_po: list[Path]
    """The path to input PO files to read, each may be a glob pattern."""
    in_iss_template: Path
    """The path to the input user-provided Liquid for the .iss script file."""
    in_isl_template: Path
    """The path to the input user-provided Liquid for the .isl messages files."""
    in_iss_path: str
    """The Liquid template resolving the output path of the .iss script file."""
    in_isl_path: str
    """The Liquid template resolving the output path of every .isl messages file."""
    out_dir: Path
    """The path of the output folder holding every rendered file."""


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
        "--iss-template",
        dest=_ISS_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input user-provided Liquid for the .iss script file.",
        metavar="FILE",
    )
    parser.add_argument(
        "--isl-template",
        dest=_ISL_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help=(
            "The path to the input user-provided Liquid for the .isl "
            "messages files."
        ),
        metavar="FILE",
    )
    parser.add_argument(
        "--iss-path",
        dest=_ISS_PATH_DEST,
        action="store",
        type=str,
        required=True,
        help=(
            "The Liquid template resolving the output path of the .iss "
            "script file, relative to the output folder."
        ),
        metavar="TEMPLATE",
    )
    parser.add_argument(
        "--isl-path",
        dest=_ISL_PATH_DEST,
        action="store",
        type=str,
        required=True,
        help=(
            "The Liquid template resolving the output path of every .isl "
            "messages file, relative to the output folder. It is rendered "
            "once per language with the language tag exposed as 'lang'."
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


def parse(args: dict[str, Any]) -> InnoRenderOpts:
    return InnoRenderOpts(
        args[_MANIFEST_DEST],
        args[_PO_DEST],
        args[_ISS_TEMPLATE_DEST],
        args[_ISL_TEMPLATE_DEST],
        args[_ISS_PATH_DEST],
        args[_ISL_PATH_DEST],
        args[_OUTPUT_DEST],
    )


class _InnoStringsView:
    """Route template string key lookups to their resolved text."""

    __pack: LanguagePack
    """The language pack the lookups route to."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack

    def __getitem__(self, key: str) -> str:
        return self.__pack.translations[key].text


class _InnoIssPathContext:
    """The Liquid-facing context of the .iss path template.

    The context is empty: the .iss path is typically a plain literal
    like 'example.iss', and referencing any variable fails the render.
    """

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ()

    def __getitem__(self, key: str) -> object:
        raise KeyError(key)


class _InnoIslPathContext:
    """The Liquid-facing context of one .isl path template rendering.

    It is rendered once per language, with the PO language tag of the
    messages file being placed exposed as ``lang``. Inno Setup has no
    standard representation of language identifiers, so no conversion
    happens: the tag is the Gettext PO tag verbatim.
    """

    __lang: str
    """The PO language tag of the .isl messages file being placed."""

    def __init__(self, lang: str):
        self.__lang = lang

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ("lang",)

    def __getitem__(self, key: str) -> object:
        if key == "lang":
            return self.__lang
        raise KeyError(key)


class _InnoIslTemplateContext:
    """The Liquid-facing top-level context of every .isl messages file
    rendering.

    The members of the current language are exposed at the top level.
    The structure is identical for every language; only the data differs.
    The class also serves as the value of ``default`` inside the .iss
    template context, where it exposes the source language the same way.
    """

    __pack: LanguagePack
    """The wrapped language pack."""
    __strings: _InnoStringsView
    """The view of the pack's translations."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack
        self.__strings = _InnoStringsView(pack)

    def keys(self) -> tuple[str, ...]:
        """Return the names of the exposed template variables."""
        return ("name", "strings")

    def __getitem__(self, key: str) -> object:
        match key:
            case "name":
                return self.__pack.lang.value
            case "strings":
                return self.__strings
            case _:
                raise KeyError(key)


class _InnoIssTemplateContext:
    """The Liquid-facing top-level context of the .iss script file
    rendering."""

    __default: _InnoIslTemplateContext
    """The view of the manifest's source language."""
    __langs: tuple[str, ...]
    """The PO language tags of every language, source language first."""

    def __init__(self, source: LanguagePack, langs: tuple[str, ...]):
        self.__default = _InnoIslTemplateContext(source)
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


def run(opts: InnoRenderOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    packs = resolve_translations(manifest, resolve_glob_files(opts.in_po))
    # The source language always leads the language list and always gets
    # an .isl messages file: its entry is the fallback localization of
    # the installer.
    source = packs.pop(manifest.source_language, None)
    if source is None:
        source = build_default_pack(manifest, manifest.source_language)
    ordered = [source, *packs.values()]
    # Inno Setup has no standard language identifier representation, so
    # the PO language tags carry over verbatim.
    langs = tuple(pack.lang.value for pack in ordered)
    logging.info("rendering languages: %s", ", ".join(langs))

    # Every component renders with its own environment, so their filters
    # never interfere with each other.
    iss_path_env = create_environment()
    register_general_filters(iss_path_env)
    isl_path_env = create_environment()
    register_general_filters(isl_path_env)
    iss_template_env = create_environment()
    register_general_filters(iss_template_env)
    register_inno_filters(iss_template_env)
    isl_template_env = create_environment()
    register_general_filters(isl_template_env)
    register_inno_filters(isl_template_env)

    iss_out = opts.out_dir / render_path(
        iss_path_env, opts.in_iss_path, _InnoIssPathContext()
    )
    iss_out.parent.mkdir(parents=True, exist_ok=True)
    render(
        iss_template_env,
        opts.in_iss_template,
        _InnoIssTemplateContext(source, langs),
        iss_out,
    )

    for pack, lang in zip(ordered, langs):
        isl_out = opts.out_dir / render_path(
            isl_path_env, opts.in_isl_path, _InnoIslPathContext(lang)
        )
        isl_out.parent.mkdir(parents=True, exist_ok=True)
        render(
            isl_template_env,
            opts.in_isl_template,
            _InnoIslTemplateContext(pack),
            isl_out,
        )
