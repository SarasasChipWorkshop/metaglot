from ...cli import DesktopPotOpts
from ...manifest import load_manifest
from ...pofile import generate_pot

def run(opts: DesktopPotOpts) -> None:
    manifest = load_manifest(opts.in_manifest)
    generate_pot(manifest, opts.out_pot)
