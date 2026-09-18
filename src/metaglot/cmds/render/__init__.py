import enum
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any
from . import rc, desktop, appstream
from .rc import RcRenderOpts
from .desktop import DesktopRenderOpts
from .appstream import AppStreamRenderOpts

_SUBCMD_DEST = "metadata"


@dataclass(frozen=True)
class RenderOpts:
    opts: RcRenderOpts | DesktopRenderOpts | AppStreamRenderOpts
    """The option of one of subcommand."""


class _Metadata(enum.StrEnum):
    Rc = "rc"
    Desktop = "desktop"
    Appstream = "appstream"


def register(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_SUBCMD_DEST, required=True)
    subcmd = cmds.add_parser(
        _Metadata.Rc.value, help="Render Windows RC resource files."
    )
    rc.register(subcmd)
    subcmd = cmds.add_parser(
        _Metadata.Desktop.value, help="Render freedesktop desktop entry files."
    )
    desktop.register(subcmd)
    subcmd = cmds.add_parser(
        _Metadata.Appstream.value, help="Render AppStream metainfo XML files."
    )
    appstream.register(subcmd)


def parse(args: dict[str, Any]) -> RenderOpts:
    match _Metadata(args[_SUBCMD_DEST]):
        case _Metadata.Rc:
            opts = RenderOpts(rc.parse(args))
        case _Metadata.Desktop:
            opts = RenderOpts(desktop.parse(args))
        case _Metadata.Appstream:
            opts = RenderOpts(appstream.parse(args))
        case _:
            raise ValueError(f"unhandled render command: {args[_SUBCMD_DEST]}")
    return opts


def run(opts: RenderOpts) -> None:
    match opts.opts:
        case RcRenderOpts() as rc_opts:
            rc.run(rc_opts)
        case DesktopRenderOpts() as desktop_opts:
            desktop.run(desktop_opts)
        case AppStreamRenderOpts() as appstream_opts:
            appstream.run(appstream_opts)
        case _:
            raise RuntimeError(f"unhandled render options: {opts.opts!r}")
