import tomllib
from pathlib import Path

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

MANIFEST_VERSION = 1
"""The manifest format version this build of MetaGlot understands."""


class StringEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    msgid: str
    context: str = ""
    comment: str = ""


class Manifest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: int
    strings: dict[str, StringEntry]

    @field_validator("version")
    @classmethod
    def _check_version(cls, value: int) -> int:
        if value != MANIFEST_VERSION:
            raise ValueError(
                f"unsupported manifest version: {value} (expected {MANIFEST_VERSION})"
            )
        return value

    @model_validator(mode="after")
    def _check_entries(self) -> "Manifest":
        empty_keys = sorted(key for key in self.strings if not key)
        if empty_keys:
            raise ValueError("string key(s) must not be empty")
        pairs = [(entry.msgid, entry.context) for entry in self.strings.values()]
        duplicated = sorted({pair for pair in pairs if pairs.count(pair) > 1})
        if duplicated:
            rendered = ", ".join(
                f"{msgid!r}" if not context else f"{msgid!r} (context {context!r})"
                for msgid, context in duplicated
            )
            raise ValueError(f"duplicated msgid and context combination(s): {rendered}")
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
