import logging
from pathlib import Path

import polib

from .manifest import Manifest, load_manifest

_POT_HEADER = {
    "Project-Id-Version": "PACKAGE VERSION",
    "PO-Revision-Date": "YEAR-MO-DA HO:MI+ZONE",
    "Last-Translator": "FULL NAME <EMAIL@ADDRESS>",
    "Language-Team": "LANGUAGE <LL@li.org>",
    "MIME-Version": "1.0",
    "Content-Type": "text/plain; charset=UTF-8",
    "Content-Transfer-Encoding": "8bit",
}


def generate(manifest_path: Path, output_path: Path) -> None:
    manifest: Manifest = load_manifest(manifest_path)
    po = polib.POFile()
    po.metadata = _POT_HEADER
    for _, entry in manifest.entries:
        po.append(
            polib.POEntry(
                msgid=entry.msgid,
                msgstr="",
                msgctxt=entry.context or None,
                comment=entry.comment or None,
            )
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    po.save(str(output_path))
    logging.info("wrote %d entries to %s", len(po), output_path)
