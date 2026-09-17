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
class RcUpdateOpts:
    in_pot: Path
    """The path to the input POT template file."""
    in_po: list[Path]
    """The path to input PO files to update, each may be a glob pattern."""


@dataclass(frozen=True)
class RcOpts:
    opts: RcPotOpts | RcRenderOpts | RcUpdateOpts
    """The option of one of subcommand."""


class RcCommand(enum.StrEnum):
    Pot = "pot"
    Render = "render"
    Update = "update"


@dataclass(frozen=True)
class DesktopPotOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    out_pot: Path
    """The path to output POT file."""


@dataclass(frozen=True)
class DesktopRenderOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    in_po: list[Path]
    """The path to input PO files to read, each may be a glob pattern."""
    in_template: Path
    """The path to the input user-provided Liquid for rendering."""
    out_desktop: Path
    """The path to the output rendered desktop entry file."""


@dataclass(frozen=True)
class DesktopUpdateOpts:
    in_pot: Path
    """The path to the input POT template file."""
    in_po: list[Path]
    """The path to input PO files to update, each may be a glob pattern."""


@dataclass(frozen=True)
class DesktopOpts:
    opts: DesktopPotOpts | DesktopRenderOpts | DesktopUpdateOpts
    """The option of one of subcommand."""


class DesktopCommand(enum.StrEnum):
    Pot = "pot"
    Render = "render"
    Update = "update"


@dataclass(frozen=True)
class AppStreamPotOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    out_pot: Path
    """The path to output POT file."""


@dataclass(frozen=True)
class AppStreamRenderOpts:
    in_manifest: Path
    """The path to input manifest file including translation strings."""
    in_po: list[Path]
    """The path to input PO files to read, each may be a glob pattern."""
    in_template: Path
    """The path to the input user-provided Liquid for rendering."""
    out_appstream: Path
    """The path to the output rendered AppStream XML file."""


@dataclass(frozen=True)
class AppStreamUpdateOpts:
    in_pot: Path
    """The path to the input POT template file."""
    in_po: list[Path]
    """The path to input PO files to update, each may be a glob pattern."""


@dataclass(frozen=True)
class AppStreamOpts:
    opts: AppStreamPotOpts | AppStreamRenderOpts | AppStreamUpdateOpts
    """The option of one of subcommand."""


class AppStreamCommand(enum.StrEnum):
    Pot = "pot"
    Render = "render"
    Update = "update"


@dataclass(frozen=True)
class Opts:
    """The root options."""

    opts: RcOpts | DesktopOpts | AppStreamOpts
    """The option of one of subcommand."""


class Command(enum.StrEnum):
    Rc = "rc"
    Desktop = "desktop"
    Appstream = "appstream"


# endregion

# region: Parameter Register

_SUBCMD_DEST = "command"
_RC_SUBCMD_DEST = "rc_command"
_DESKTOP_SUBCMD_DEST = "desktop_command"


_RC_POT_MANIFEST_DEST = "manifest"
_RC_POT_OUTPUT_DEST = "output"

_RC_RDR_MANIFEST_DEST = "manifest"
_RC_RDR_PO_DEST = "po"
_RC_RDR_TEMPLATE_DEST = "template"
_RC_RDR_OUTPUT_DEST = "output"

_RC_UPD_POT_DEST = "pot"
_RC_UPD_PO_DEST = "po"

_DESKTOP_POT_MANIFEST_DEST = "manifest"
_DESKTOP_POT_OUTPUT_DEST = "output"

_DESKTOP_RDR_MANIFEST_DEST = "manifest"
_DESKTOP_RDR_PO_DEST = "po"
_DESKTOP_RDR_TEMPLATE_DEST = "template"
_DESKTOP_RDR_OUTPUT_DEST = "output"

_DESKTOP_UPD_POT_DEST = "pot"
_DESKTOP_UPD_PO_DEST = "po"

_APPSTREAM_SUBCMD_DEST = "appstream_command"

_APPSTREAM_POT_MANIFEST_DEST = "manifest"
_APPSTREAM_POT_OUTPUT_DEST = "output"

_APPSTREAM_RDR_MANIFEST_DEST = "manifest"
_APPSTREAM_RDR_PO_DEST = "po"
_APPSTREAM_RDR_TEMPLATE_DEST = "template"
_APPSTREAM_RDR_OUTPUT_DEST = "output"

_APPSTREAM_UPD_POT_DEST = "pot"
_APPSTREAM_UPD_PO_DEST = "po"


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


def _register_rc_update_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-t",
        "--pot",
        dest=_RC_UPD_POT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input POT template file.",
        metavar="FILE",
    )
    parser.add_argument(
        "-p",
        "--po",
        dest=_RC_UPD_PO_DEST,
        action="extend",
        nargs="+",
        type=Path,
        required=True,
        help="The PO files to update, each may be a glob pattern.",
        metavar="GLOB",
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
    update_subcmd = cmds.add_parser(
        RcCommand.Update.value, help="Update PO files against a POT template."
    )
    _register_rc_update_param(update_subcmd)


def _register_desktop_pot_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--manifest",
        dest=_DESKTOP_POT_MANIFEST_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to input manifest file including translation strings.",
        metavar="FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest=_DESKTOP_POT_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to output POT file.",
        metavar="FILE",
    )


def _register_desktop_render_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--manifest",
        dest=_DESKTOP_RDR_MANIFEST_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to input manifest file including translation strings.",
        metavar="FILE",
    )
    parser.add_argument(
        "-p",
        "--po",
        dest=_DESKTOP_RDR_PO_DEST,
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
        dest=_DESKTOP_RDR_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input user-provided Liquid for rendering.",
        metavar="FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest=_DESKTOP_RDR_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the output rendered desktop entry file.",
        metavar="FILE",
    )


def _register_desktop_update_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-t",
        "--pot",
        dest=_DESKTOP_UPD_POT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input POT template file.",
        metavar="FILE",
    )
    parser.add_argument(
        "-p",
        "--po",
        dest=_DESKTOP_UPD_PO_DEST,
        action="extend",
        nargs="+",
        type=Path,
        required=True,
        help="The PO files to update, each may be a glob pattern.",
        metavar="GLOB",
    )


def _register_desktop_param(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_DESKTOP_SUBCMD_DEST, required=True)
    pot_subcmd = cmds.add_parser(
        DesktopCommand.Pot.value,
        help="Generate a POT template from given manifest.",
    )
    _register_desktop_pot_param(pot_subcmd)
    render_subcmd = cmds.add_parser(
        DesktopCommand.Render.value,
        help="Render a user-provided template with manifest data and PO translations.",
    )
    _register_desktop_render_param(render_subcmd)
    update_subcmd = cmds.add_parser(
        DesktopCommand.Update.value, help="Update PO files against a POT template."
    )
    _register_desktop_update_param(update_subcmd)


def _register_appstream_pot_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--manifest",
        dest=_APPSTREAM_POT_MANIFEST_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to input manifest file including translation strings.",
        metavar="FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest=_APPSTREAM_POT_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to output POT file.",
        metavar="FILE",
    )


def _register_appstream_render_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-m",
        "--manifest",
        dest=_APPSTREAM_RDR_MANIFEST_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to input manifest file including translation strings.",
        metavar="FILE",
    )
    parser.add_argument(
        "-p",
        "--po",
        dest=_APPSTREAM_RDR_PO_DEST,
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
        dest=_APPSTREAM_RDR_TEMPLATE_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input user-provided Liquid for rendering.",
        metavar="FILE",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest=_APPSTREAM_RDR_OUTPUT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the output rendered AppStream XML file.",
        metavar="FILE",
    )


def _register_appstream_update_param(parser: ArgumentParser) -> None:
    parser.add_argument(
        "-t",
        "--pot",
        dest=_APPSTREAM_UPD_POT_DEST,
        action="store",
        type=Path,
        required=True,
        help="The path to the input POT template file.",
        metavar="FILE",
    )
    parser.add_argument(
        "-p",
        "--po",
        dest=_APPSTREAM_UPD_PO_DEST,
        action="extend",
        nargs="+",
        type=Path,
        required=True,
        help="The PO files to update, each may be a glob pattern.",
        metavar="GLOB",
    )


def _register_appstream_param(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_APPSTREAM_SUBCMD_DEST, required=True)
    pot_subcmd = cmds.add_parser(
        AppStreamCommand.Pot.value,
        help="Generate a POT template from given manifest.",
    )
    _register_appstream_pot_param(pot_subcmd)
    render_subcmd = cmds.add_parser(
        AppStreamCommand.Render.value,
        help="Render a user-provided template with manifest data and PO translations.",
    )
    _register_appstream_render_param(render_subcmd)
    update_subcmd = cmds.add_parser(
        AppStreamCommand.Update.value, help="Update PO files against a POT template."
    )
    _register_appstream_update_param(update_subcmd)


def _register_param(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_SUBCMD_DEST, required=True)
    rc_subcmd = cmds.add_parser(
        Command.Rc.value, help="Commands for Windows RC resource files."
    )
    _register_rc_param(rc_subcmd)
    desktop_subcmd = cmds.add_parser(
        Command.Desktop.value, help="Commands for freedesktop desktop entry files."
    )
    _register_desktop_param(desktop_subcmd)
    appstream_subcmd = cmds.add_parser(
        Command.Appstream.value, help="Commands for AppStream metainfo XML files."
    )
    _register_appstream_param(appstream_subcmd)


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
                case RcCommand.Update:
                    rc_upd_opts = RcUpdateOpts(
                        args[_RC_UPD_POT_DEST], args[_RC_UPD_PO_DEST]
                    )
                    rc_opts = RcOpts(rc_upd_opts)
                case _:
                    raise ValueError(f"unhandled rc command: {args[_RC_SUBCMD_DEST]}")
            opts = Opts(rc_opts)
        case Command.Desktop:
            match DesktopCommand(args[_DESKTOP_SUBCMD_DEST]):
                case DesktopCommand.Pot:
                    desktop_pot_opts = DesktopPotOpts(
                        args[_DESKTOP_POT_MANIFEST_DEST], args[_DESKTOP_POT_OUTPUT_DEST]
                    )
                    desktop_opts = DesktopOpts(desktop_pot_opts)
                case DesktopCommand.Render:
                    desktop_rdr_opts = DesktopRenderOpts(
                        args[_DESKTOP_RDR_MANIFEST_DEST],
                        args[_DESKTOP_RDR_PO_DEST],
                        args[_DESKTOP_RDR_TEMPLATE_DEST],
                        args[_DESKTOP_RDR_OUTPUT_DEST],
                    )
                    desktop_opts = DesktopOpts(desktop_rdr_opts)
                case DesktopCommand.Update:
                    desktop_upd_opts = DesktopUpdateOpts(
                        args[_DESKTOP_UPD_POT_DEST], args[_DESKTOP_UPD_PO_DEST]
                    )
                    desktop_opts = DesktopOpts(desktop_upd_opts)
                case _:
                    raise ValueError(
                        f"unhandled desktop command: {args[_DESKTOP_SUBCMD_DEST]}"
                    )
            opts = Opts(desktop_opts)
        case Command.Appstream:
            match AppStreamCommand(args[_APPSTREAM_SUBCMD_DEST]):
                case AppStreamCommand.Pot:
                    appstream_pot_opts = AppStreamPotOpts(
                        args[_APPSTREAM_POT_MANIFEST_DEST],
                        args[_APPSTREAM_POT_OUTPUT_DEST],
                    )
                    appstream_opts = AppStreamOpts(appstream_pot_opts)
                case AppStreamCommand.Render:
                    appstream_rdr_opts = AppStreamRenderOpts(
                        args[_APPSTREAM_RDR_MANIFEST_DEST],
                        args[_APPSTREAM_RDR_PO_DEST],
                        args[_APPSTREAM_RDR_TEMPLATE_DEST],
                        args[_APPSTREAM_RDR_OUTPUT_DEST],
                    )
                    appstream_opts = AppStreamOpts(appstream_rdr_opts)
                case AppStreamCommand.Update:
                    appstream_upd_opts = AppStreamUpdateOpts(
                        args[_APPSTREAM_UPD_POT_DEST], args[_APPSTREAM_UPD_PO_DEST]
                    )
                    appstream_opts = AppStreamOpts(appstream_upd_opts)
                case _:
                    raise ValueError(
                        f"unhandled appstream command: {args[_APPSTREAM_SUBCMD_DEST]}"
                    )
            opts = Opts(appstream_opts)
        case _:
            raise ValueError(f"unhandled command: {args[_SUBCMD_DEST]}")
    return opts
