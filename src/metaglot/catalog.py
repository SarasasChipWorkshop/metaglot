import glob
import tomllib
from pathlib import Path

import polib
from pydantic import BaseModel, ConfigDict, model_validator


class StringEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    msgid: str
    context: str = ""


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    strings: dict[str, StringEntry]

    @model_validator(mode="after")
    def _check_entries(self) -> "Manifest":
        empty_keys = sorted(key for key in self.strings if not key)
        if empty_keys:
            raise ValueError("string key(s) must not be empty")
        msgids = [entry.msgid for entry in self.strings.values()]
        duplicated_msgids = sorted({msgid for msgid in msgids if msgids.count(msgid) > 1})
        if duplicated_msgids:
            raise ValueError(f"duplicated msgid(s): {', '.join(duplicated_msgids)}")
        return self

    @property
    def entries(self) -> list[tuple[str, StringEntry]]:
        return list(self.strings.items())

    @property
    def msgids(self) -> set[str]:
        return {entry.msgid for entry in self.strings.values()}


def load_manifest(path: Path) -> Manifest:
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"failed to parse manifest '{path}': {exc}") from exc
    except OSError as exc:
        raise RuntimeError(f"failed to read manifest '{path}': {exc}") from exc
    return Manifest.model_validate(raw)


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
