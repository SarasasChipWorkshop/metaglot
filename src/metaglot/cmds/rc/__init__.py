import enum
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any
from . import pot, render, update
from .pot import RcPotOpts
from .render import RcRenderOpts
from .update import RcUpdateOpts

_SUBCMD_DEST = "subcommand"


@dataclass(frozen=True)
class RcOpts:
    opts: RcPotOpts | RcRenderOpts | RcUpdateOpts
    """The option of one of subcommand."""


class _Command(enum.StrEnum):
    Pot = "pot"
    Render = "render"
    Update = "update"


def register(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_SUBCMD_DEST, required=True)
    pot_subcmd = cmds.add_parser(
        _Command.Pot.value, help="Generate a POT template from given manifest."
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


def parse(args: dict[str, Any]) -> RcOpts:
    match _Command(args[_SUBCMD_DEST]):
        case _Command.Pot:
            opts = RcOpts(pot.parse(args))
        case _Command.Render:
            opts = RcOpts(render.parse(args))
        case _Command.Update:
            opts = RcOpts(update.parse(args))
        case _:
            raise ValueError(f"unhandled rc command: {args[_SUBCMD_DEST]}")
    return opts


def run(opts: RcOpts) -> None:
    match opts.opts:
        case RcPotOpts() as pot_opts:
            pot.run(pot_opts)
        case RcRenderOpts() as render_opts:
            render.run(render_opts)
        case RcUpdateOpts() as update_opts:
            update.run(update_opts)
        case _:
            raise RuntimeError(f"unhandled rc options: {opts.opts!r}")
