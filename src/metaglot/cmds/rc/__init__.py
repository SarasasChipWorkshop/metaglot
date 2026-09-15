from ...cli import RcOpts, RcPotOpts, RcRenderOpts, RcUpdateOpts
from . import pot, render, update

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
