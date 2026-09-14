import enum
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

# region: Options and Commands


@dataclass(frozen=True)
class RcPotOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    out_pot: Path
    """The path to output POT file."""


@dataclass(frozen=True)
class RcRenderOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    in_po: list[Path]
    """The path to input PO files to read, each may be a glob pattern."""
    in_template: Path
    """The path to the input user-provided Liquid for rendering."""
    out_rc: Path
    """The path to the output rendered Windows RC file."""


@dataclass(frozen=True)
class RcOpts:
    opts: RcPotOpts | RcRenderOpts
    """The option of one of subcommand."""


class RcCommand(enum.StrEnum):
    Pot = "pot"
    Render = "render"


@dataclass(frozen=True)
class Opts:
    """The root options."""

    opts: RcOpts
    """The option of one of subcommand."""


class Command(enum.StrEnum):
    Rc = "rc"


# endregion

# region: Parameter Register

_SUBCMD_DEST = "command"
_RC_SUBCMD_DEST = "rc_command"


_RC_POT_MANIFEST_DEST = "manifest"
_RC_POT_OUTPUT_DEST = "output"

_RC_RDR_MANIFEST_DEST = "manifest"
_RC_RDR_PO_DEST = "po"
_RC_RDR_TEMPLATE_DEST = "template"
_RC_RDR_OUTPUT_DEST = "output"


def _register_rc_pot_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--manifest",
        dest=_RC_POT_MANIFEST_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to input manifest file including translation strings.",
        metavar="FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest=_RC_POT_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to output POT file.",
        metavar="FILE",
    )


def _register_rc_render_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--manifest",
        dest=_RC_RDR_MANIFEST_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to input manifest file including translation strings.",
        metavar="FILE",
    )
    parser.add_argument(
        "-p",
        "--po",
        dest=_RC_RDR_PO_DEST,
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
        dest=_RC_RDR_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input user-provided Liquid for rendering.",
        metavar="FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest=_RC_RDR_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the output rendered Windows RC file.",
        metavar="FILE",
    )


def _register_rc_param(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_RC_SUBCMD_DEST, required=True)
    pot_subcmd = cmds.add_parser(
        RcCommand.Pot.value, help="Generate a POT template from given manifest."
    )
    _register_rc_pot_param(pot_subcmd)
    render_subcmd = cmds.add_parser(
        RcCommand.Render.value,
        help="Render a user-provided template with manifest data and PO translations.",
    )
    _register_rc_render_param(render_subcmd)


def _register_param(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_SUBCMD_DEST, required=True)
    rc_subcmd = cmds.add_parser(
        Command.Rc.value, help="Commands for Windows RC resource files."
    )
    _register_rc_param(rc_subcmd)


# endregion


def parse() -> Opts:
    """
    Parse MetaGlot command line options.

    :return: The parsed command line options.
    """
    parser = ArgumentParser(
        prog="metaglot",
        description="A command-line tool that unifies localization metadata for applications shipped on multiple platforms.",
    )
    _register_param(parser)

    args = vars(parser.parse_args())

    match Command(args[_SUBCMD_DEST]):
        case Command.Rc:
            match RcCommand(args[_RC_SUBCMD_DEST]):
                case RcCommand.Pot:
                    rc_pot_opts = RcPotOpts(
                        args[_RC_POT_MANIFEST_DEST], args[_RC_POT_OUTPUT_DEST]
                    )
                    rc_opts = RcOpts(rc_pot_opts)
                case RcCommand.Render:
                    rc_rdr_opts = RcRenderOpts(
                        args[_RC_RDR_MANIFEST_DEST],
                        args[_RC_RDR_PO_DEST],
                        args[_RC_RDR_TEMPLATE_DEST],
                        args[_RC_RDR_OUTPUT_DEST],
                    )
                    rc_opts = RcOpts(rc_rdr_opts)
                case _:
                    raise ValueError(f"unhandled rc command: {args[_RC_SUBCMD_DEST]}")
            opts = Opts(rc_opts)
        case _:
            raise ValueError(f"unhandled command: {args[_SUBCMD_DEST]}")
    return opts
