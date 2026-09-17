from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ...manifest import load_manifest
from ...pofile import generate_pot

_MANIFEST_DEST = "manifest"
_OUTPUT_DEST = "output"


@dataclass(frozen=True)
class DesktopPotOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    out_pot: Path
    """The path to output POT file."""


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
        "-o",
        "--output",
        dest=_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to output POT file.",
        metavar="FILE",
    )


def parse(args: dict[str, Any]) -> DesktopPotOpts:
    return DesktopPotOpts(args[_MANIFEST_DEST], args[_OUTPUT_DEST])


def run(opts: DesktopPotOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    generate_pot(manifest, opts.out_pot)
