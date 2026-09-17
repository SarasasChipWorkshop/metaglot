from ...cli import DesktopOpts, DesktopPotOpts, DesktopRenderOpts, DesktopUpdateOpts
from . import pot, render, update

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
