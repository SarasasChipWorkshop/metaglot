from ...cli import RcPotOpts
from ...manifest import load_manifest
from ...pofile import generate_pot

def run(opts: RcPotOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    generate_pot(manifest, opts.out_pot)
