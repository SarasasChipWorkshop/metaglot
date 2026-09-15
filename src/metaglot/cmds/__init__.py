from ..cli import Opts, RcOpts
from . import rc

def run(opts: Opts) -> None:
    match opts.opts:
        case RcOpts() as rc_opts:
            rc.run(rc_opts)
        case _:
            raise RuntimeError(f"unhandled options: {opts.opts!r}")
