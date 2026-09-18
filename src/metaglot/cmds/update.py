from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from ..pofile import resolve_glob_files, update_po_files

_POT_DEST = "pot"
_PO_DEST = "po"


@dataclass(frozen=True)
class UpdateOpts:
    in_pot: Path
    """The path to the input POT template file."""
    in_po: list[Path]
    """The path to input PO files to update, each may be a glob pattern."""


def register(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-t",
        "--pot",
        dest=_POT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input POT template file.",
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
        help="The PO files to update, each may be a glob pattern.",
        metavar="GLOB",
    )


def parse(args: dict[str, Any]) -> UpdateOpts:
    return UpdateOpts(args[_POT_DEST], args[_PO_DEST])


def run(opts: UpdateOpts) -> None:
    update_po_files(opts.in_pot, resolve_glob_files(opts.in_po))
