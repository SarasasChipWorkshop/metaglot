import tomllib
from typing import Optional
from pathlib import Path
from pydantic import BaseModel, ConfigDict, field_validator, model_validator

MANIFEST_VERSION = 1
"""The manifest format version this build of MetaGlot understands."""


class StringEntry(BaseModel, frozen=True):
    model_config = ConfigDict(extra="forbid", strict=True)

    msgid: str
    """The string to be translated."""
    context: Optional[str] = None
    """The context of this entry. ``None`` if no context."""
    comment: Optional[str] = None
    """Translator-oriented comment of this entry. ``None`` if nothing."""


class Manifest(BaseModel, frozen=True):
    model_config = ConfigDict(extra="forbid", strict=True)

    version: int
    """The version of this manifest file."""
    strings: dict[str, StringEntry]
    """The list holding all strings to be translated."""

    @field_validator("version")
    def validate_version(cls, value: int) -> int:
        if value != MANIFEST_VERSION:
            raise ValueError(
                f"unsupported manifest version: {value} (expected {MANIFEST_VERSION})"
            )
        return value

    @model_validator(mode="after")
    def validate_string_entries(self) -> "Manifest":
        has_empty_key = any(key == "" for key in self.strings.keys())
        if has_empty_key:
            raise ValueError("string key(s) must not be empty")

        has_empty_value = any(value.msgid == "" for value in self.strings.values())
        if has_empty_value:
            raise ValueError("string value(s) must not be empty")

        seen: set[tuple[str, Optional[str]]] = set()
        duplicates: set[tuple[str, Optional[str]]] = set()
        for entry in self.strings.values():
            pair = (entry.msgid, entry.context)
            if pair in seen:
                duplicates.add(pair)
            seen.add(pair)
        if duplicates:
            rendered = ", ".join(
                f"{msgid!r}" if context is None else f"{msgid!r} (context {context!r})"
                for msgid, context in sorted(
                    duplicates, key=lambda pair: (pair[0], pair[1] or "")
                )
            )
            raise ValueError(f"duplicated msgid and context combination(s): {rendered}")

        return self


def load_manifest(path: Path) -> Manifest:
    try:
        with open(path, "rb") as f:
            raw = tomllib.load(f)
            return Manifest.model_validate(raw)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"failed to parse manifest '{path}': {exc}") from exc
    except OSError as exc:
        raise RuntimeError(f"failed to read manifest '{path}': {exc}") from exc
