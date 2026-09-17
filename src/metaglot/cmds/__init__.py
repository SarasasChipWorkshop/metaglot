import enum
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any
from . import appstream, desktop, rc
from .rc import RcOpts
from .desktop import DesktopOpts
from .appstream import AppStreamOpts


@dataclass(frozen=True)
class Opts:
    """The root options."""

    opts: RcOpts | DesktopOpts | AppStreamOpts
    """The option of one of subcommand."""


_SUBCMD_DEST = "command"


class _Command(enum.StrEnum):
    Rc = "rc"
    Desktop = "desktop"
    Appstream = "appstream"


def register(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_SUBCMD_DEST, required=True)
    subcmd = cmds.add_parser(
        _Command.Rc.value, help="Commands for Windows RC resource files."
    )
    rc.register(subcmd)
    subcmd = cmds.add_parser(
        _Command.Desktop.value, help="Commands for freedesktop desktop entry files."
    )
    desktop.register(subcmd)
    subcmd = cmds.add_parser(
        _Command.Appstream.value, help="Commands for AppStream metainfo XML files."
    )
    appstream.register(subcmd)


def parse(args: dict[str, Any]) -> Opts:
    match _Command(args[_SUBCMD_DEST]):
        case _Command.Rc:
            opts = Opts(rc.parse(args))
        case _Command.Desktop:
            opts = Opts(desktop.parse(args))
        case _Command.Appstream:
            opts = Opts(appstream.parse(args))
        case _:
            raise ValueError(f"unhandled command: {args[_SUBCMD_DEST]}")
    return opts


def run(opts: Opts) -> None:
    match opts.opts:
        case RcOpts() as rc_opts:
            rc.run(rc_opts)
        case DesktopOpts() as desktop_opts:
            desktop.run(desktop_opts)
        case AppStreamOpts() as appstream_opts:
            appstream.run(appstream_opts)
        case _:
            raise RuntimeError(f"unhandled options: {opts.opts!r}")
