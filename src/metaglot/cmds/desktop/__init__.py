import enum
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any
from . import pot, render, update
from .pot import DesktopPotOpts
from .render import DesktopRenderOpts
from .update import DesktopUpdateOpts

_SUBCMD_DEST = "subcommand"


@dataclass(frozen=True)
class DesktopOpts:
    opts: DesktopPotOpts | DesktopRenderOpts | DesktopUpdateOpts
    """The option of one of subcommand."""


class _Command(enum.StrEnum):
    Pot = "pot"
    Render = "render"
    Update = "update"


def register(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_SUBCMD_DEST, required=True)
    pot_subcmd = cmds.add_parser(
        _Command.Pot.value,
        help="Generate a POT template from given manifest.",
    )
    pot.register(pot_subcmd)
    render_subcmd = cmds.add_parser(
        _Command.Render.value,
        help="Render a user-provided template with manifest data and PO translations.",
    )
    render.register(render_subcmd)
    update_subcmd = cmds.add_parser(
        _Command.Update.value, help="Update PO files against a POT template."
    )
    update.register(update_subcmd)


def parse(args: dict[str, Any]) -> DesktopOpts:
    match _Command(args[_SUBCMD_DEST]):
        case _Command.Pot:
            opts = DesktopOpts(pot.parse(args))
        case _Command.Render:
            opts = DesktopOpts(render.parse(args))
        case _Command.Update:
            opts = DesktopOpts(update.parse(args))
        case _:
            raise ValueError(
                f"unhandled desktop command: {args[_SUBCMD_DEST]}"
            )
    return opts


def run(opts: DesktopOpts) -> None:
    match opts.opts:
        case DesktopPotOpts() as pot_opts:
            pot.run(pot_opts)
        case DesktopRenderOpts() as render_opts:
            render.run(render_opts)
        case DesktopUpdateOpts() as update_opts:
            update.run(update_opts)
        case _:
            raise RuntimeError(f"unhandled desktop options: {opts.opts!r}")
