from ...cli import RcUpdateOpts
from ...pofile import resolve_glob_files, update_po_files


def run(opts: RcUpdateOpts) -> None:
    update_po_files(opts.in_pot, resolve_glob_files(opts.in_po))
