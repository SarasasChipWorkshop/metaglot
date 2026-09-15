from ...cli import RcOpts, RcPotOpts, RcRenderOpts
from . import pot, render

def run(opts: RcOpts) -> None:
    match opts.opts:
        case RcPotOpts() as pot_opts:
            pot.run(pot_opts)
        case RcRenderOpts() as render_opts:
            render.run(render_opts)
        case _:
            raise RuntimeError(f"unhandled rc options: {opts.opts!r}")

