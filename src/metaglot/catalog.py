import glob
from pathlib import Path

import polib


def collect_po_files(patterns: list[Path]) -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        matched = sorted(glob.glob(str(pattern)))
        if not matched:
            raise ValueError(f"the pattern '{pattern}' matched no PO file")
        for name in matched:
            file = Path(name)
            resolved = file.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(file)
    return files


def load_po(path: Path) -> tuple[str, dict[str, str]]:
    try:
        po = polib.pofile(str(path))
    except (OSError, IOError) as exc:
        raise RuntimeError(f"failed to read PO file '{path}': {exc}") from exc
    locale = po.metadata.get("Language") or path.stem
    translations = {
        entry.msgid: entry.msgstr
        for entry in po
        if entry.msgstr and "fuzzy" not in entry.flags
    }
    return locale, translations
