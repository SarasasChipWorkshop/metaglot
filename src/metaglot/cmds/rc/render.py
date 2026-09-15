from ...cli import RcRenderOpts
from ...render import render


def run(opts: RcRenderOpts) -> None:
    render(
        opts.in_manifest,
        opts.in_po,
        opts.in_template,
        opts.out_rc,
    )
