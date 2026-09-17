from ..cli import Opts, RcOpts, DesktopOpts, AppStreamOpts
from . import appstream, desktop, rc

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
