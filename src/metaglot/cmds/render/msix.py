import logging
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ...filters import (
    register_general_filters,
    register_msix_manifest_filters,
    register_msix_resources_filters,
)
from ...langmap import msix_lang_map
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
_MANIFEST_TEMPLATE_DEST = "manifest_template"
_RESOURCES_TEMPLATE_DEST = "resources_template"
_MANIFEST_PATH_DEST = "manifest_path"
_RESOURCES_PATH_DEST = "resources_path"
_OUTPUT_DEST = "output"


@dataclass(frozen=True)
class MsixRenderOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    in_po: list[Path]
    """The path to input PO files to read, each may be a glob pattern."""
    in_manifest_template: Path
    """The path to the input user-provided Liquid for the manifest file."""
    in_resources_template: Path
    """The path to the input user-provided Liquid for the resources files."""
    in_manifest_path: str
    """The Liquid template resolving the output path of the manifest file."""
    in_resources_path: str
    """The Liquid template resolving the output path of every resources file."""
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
        "--manifest-template",
        dest=_MANIFEST_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input user-provided Liquid for the manifest file.",
        metavar="FILE",
    )
    parser.add_argument(
        "--resources-template",
        dest=_RESOURCES_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input user-provided Liquid for the resources files.",
        metavar="FILE",
    )
    parser.add_argument(
        "--manifest-path",
        dest=_MANIFEST_PATH_DEST,
        action="store",
        type=str,
        required=True,
        help=(
            "The Liquid template resolving the output path of the manifest file, "
            "relative to the output folder."
        ),
        metavar="TEMPLATE",
    )
    parser.add_argument(
        "--resources-path",
        dest=_RESOURCES_PATH_DEST,
        action="store",
        type=str,
        required=True,
        help=(
            "The Liquid template resolving the output path of every resources "
            "file, relative to the output folder. It is rendered once per "
            "language with the language tag exposed as 'lang'."
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


def parse(args: dict[str, Any]) -> MsixRenderOpts:
    return MsixRenderOpts(
        args[_MANIFEST_DEST],
        args[_PO_DEST],
        args[_MANIFEST_TEMPLATE_DEST],
        args[_RESOURCES_TEMPLATE_DEST],
        args[_MANIFEST_PATH_DEST],
        args[_RESOURCES_PATH_DEST],
        args[_OUTPUT_DEST],
    )


class _MsixStringsView:
    """Route template string key lookups to their resolved text."""

    __pack: LanguagePack
    """The language pack the lookups route to."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack

    def __getitem__(self, key: str) -> str:
        return self.__pack.translations[key].text


class _MsixManifestPathContext:
    """The Liquid-facing context of the manifest path template.

    The context is empty: the manifest path is typically the plain
    literal 'AppxManifest.xml', and referencing any variable fails
    the render.
    """

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ()

    def __getitem__(self, key: str) -> object:
        raise KeyError(key)


class _MsixResourcesPathContext:
    """The Liquid-facing context of one resources path template rendering.

    It is rendered once per language, with the language tag of the
    resources file being placed exposed as ``lang``.
    """

    __lang: str
    """The BCP 47 language tag of the resources file being placed."""

    def __init__(self, lang: str):
        self.__lang = lang

    def keys(self) -> tuple[str, ...]:
        """Return the names of the top-level template variables."""
        return ("lang",)

    def __getitem__(self, key: str) -> object:
        if key == "lang":
            return self.__lang
        raise KeyError(key)


class _MsixResourcesTemplateContext:
    """The Liquid-facing top-level context of every resources file rendering.

    The members of the current language are exposed at the top level.
    The structure is identical for every language; only the data differs.
    The class also serves as the value of ``default`` inside the manifest
    template context, where it exposes the source language the same way.
    """

    __pack: LanguagePack
    """The wrapped language pack."""
    __strings: _MsixStringsView
    """The view of the pack's translations."""
    __lang: str
    """The BCP 47 language tag of the pack's language."""

    def __init__(self, pack: LanguagePack):
        self.__pack = pack
        self.__strings = _MsixStringsView(pack)
        self.__lang = msix_lang_map.convert(pack.lang).value

    def keys(self) -> tuple[str, ...]:
        """Return the names of the exposed template variables."""
        return ("name", "lang", "strings")

    def __getitem__(self, key: str) -> object:
        match key:
            case "name":
                return self.__pack.lang.value
            case "lang":
                return self.__lang
            case "strings":
                return self.__strings
            case _:
                raise KeyError(key)


class _MsixManifestTemplateContext:
    """The Liquid-facing top-level context of the manifest file rendering."""

    __default: _MsixResourcesTemplateContext
    """The view of the manifest's source language."""
    __langs: tuple[str, ...]
    """The BCP 47 language tags of every language, source language first."""

    def __init__(self, source: LanguagePack, langs: tuple[str, ...]):
        self.__default = _MsixResourcesTemplateContext(source)
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


def run(opts: MsixRenderOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    packs = resolve_translations(manifest, resolve_glob_files(opts.in_po))
    # The source language always leads the language list: MSIX takes the
    # first listed language as the default one, and its resources folder
    # is the fallback for every other language.
    source = packs.pop(manifest.source_language, None)
    if source is None:
        source = build_default_pack(manifest, manifest.source_language)
    ordered = [source, *packs.values()]
    langs = tuple(msix_lang_map.convert(pack.lang).value for pack in ordered)
    logging.info("rendering languages: %s", ", ".join(langs))

    # Every component renders with its own environment, so their filters
    # never interfere with each other.
    manifest_path_env = create_environment()
    register_general_filters(manifest_path_env)
    resources_path_env = create_environment()
    register_general_filters(resources_path_env)
    manifest_template_env = create_environment()
    register_general_filters(manifest_template_env)
    register_msix_manifest_filters(manifest_template_env)
    resources_template_env = create_environment()
    register_general_filters(resources_template_env)
    register_msix_resources_filters(resources_template_env)

    manifest_out = opts.out_dir / render_path(
        manifest_path_env, opts.in_manifest_path, _MsixManifestPathContext()
    )
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    render(
        manifest_template_env,
        opts.in_manifest_template,
        _MsixManifestTemplateContext(source, langs),
        manifest_out,
    )

    for pack, lang in zip(ordered, langs):
        resources_out = opts.out_dir / render_path(
            resources_path_env,
            opts.in_resources_path,
            _MsixResourcesPathContext(lang),
        )
        resources_out.parent.mkdir(parents=True, exist_ok=True)
        render(
            resources_template_env,
            opts.in_resources_template,
            _MsixResourcesTemplateContext(pack),
            resources_out,
        )
