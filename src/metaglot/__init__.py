import logging
import sys

from . import pofile, render
from .cli import parse, RcOpts, RcPotOpts, RcRenderOpts
from .manifest import load_manifest


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    opts = parse()

    try:
        match opts.opts:
            case RcOpts() as rc_opts:
                match rc_opts.opts:
                    case RcPotOpts() as rc_pot_opts:
                        manifest = load_manifest(rc_pot_opts.in_manifest)
                        pofile.generate_pot(manifest, rc_pot_opts.out_pot)
                    case RcRenderOpts() as rc_rdr_opts:
                        render.render(
                            rc_rdr_opts.in_manifest,
                            rc_rdr_opts.in_po,
                            rc_rdr_opts.in_template,
                            rc_rdr_opts.out_rc,
                        )
                    case _:
                        raise RuntimeError(f"unhandled rc options: {rc_opts.opts!r}")
            case _:
                raise RuntimeError(f"unhandled options: {opts.opts!r}")
    except Exception as e:
        logging.fatal("Runtime error: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
