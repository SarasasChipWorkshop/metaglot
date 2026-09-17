from ...cli import AppStreamPotOpts
from ...manifest import load_manifest
from ...pofile import generate_pot

def run(opts: AppStreamPotOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    generate_pot(manifest, opts.out_pot)
