import enum
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any
from . import pot, update, render
from .pot import PotOpts
from .update import UpdateOpts
from .render import RenderOpts


@dataclass(frozen=True)
class Opts:
    """The root options."""

    opts: PotOpts | UpdateOpts | RenderOpts
    """The option of one of subcommand."""


_SUBCMD_DEST = "command"


class _Command(enum.StrEnum):
    Pot = "pot"
    Update = "update"
    Render = "render"


def register(parser: ArgumentParser) -> None:
    cmds = parser.add_subparsers(dest=_SUBCMD_DEST, required=True)
    subcmd = cmds.add_parser(
        _Command.Pot.value, help="Generate a POT template from given manifest."
    )
    pot.register(subcmd)
    subcmd = cmds.add_parser(
        _Command.Update.value, help="Update PO files against a POT template."
    )
    update.register(subcmd)
    subcmd = cmds.add_parser(
        _Command.Render.value,
        help="Render a user-provided template with manifest data and PO translations.",
    )
    render.register(subcmd)


def parse(args: dict[str, Any]) -> Opts:
    match _Command(args[_SUBCMD_DEST]):
        case _Command.Pot:
            opts = Opts(pot.parse(args))
        case _Command.Update:
            opts = Opts(update.parse(args))
        case _Command.Render:
            opts = Opts(render.parse(args))
        case _:
            raise ValueError(f"unhandled command: {args[_SUBCMD_DEST]}")
    return opts


def run(opts: Opts) -> None:
    match opts.opts:
        case PotOpts() as pot_opts:
            pot.run(pot_opts)
        case UpdateOpts() as update_opts:
            update.run(update_opts)
        case RenderOpts() as render_opts:
            render.run(render_opts)
        case _:
            raise RuntimeError(f"unhandled options: {opts.opts!r}")
