from ...cli import (
    AppStreamOpts,
    AppStreamPotOpts,
    AppStreamRenderOpts,
    AppStreamUpdateOpts,
)
from . import pot, render, update

def run(opts: AppStreamOpts) -> None:
    match opts.opts:
        case AppStreamPotOpts() as pot_opts:
            pot.run(pot_opts)
        case AppStreamRenderOpts() as render_opts:
            render.run(render_opts)
        case AppStreamUpdateOpts() as update_opts:
            update.run(update_opts)
        case _:
            raise RuntimeError(f"unhandled appstream options: {opts.opts!r}")
