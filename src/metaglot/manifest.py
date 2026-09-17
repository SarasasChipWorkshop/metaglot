import tomllib
from typing import Annotated, Optional
from pathlib import Path
from pydantic import (
    BaseModel,
    ConfigDict,
    GetPydanticSchema,
    field_validator,
    model_validator,
)
from pydantic_core import core_schema

from .langid import PoLang

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


def _validate_po_lang(value) -> PoLang:
    if isinstance(value, PoLang):
        return value
    return PoLang(value)


def _po_lang_schema(source_type, handler) -> core_schema.CoreSchema:
    """Describe how pydantic validates a ``PoLang`` field.

    The whole validation is delegated to :func:`_validate_po_lang`, which
    accepts any value parseable by ``PoLang``. This keeps the field typed
    as ``PoLang`` without enabling ``arbitrary_types_allowed`` on the model.
    """
    return core_schema.no_info_plain_validator_function(
        _validate_po_lang,
        serialization=core_schema.to_string_ser_schema(),
    )


class Manifest(BaseModel, frozen=True):
    model_config = ConfigDict(extra="forbid", strict=True)

    version: int
    """The version of this manifest file."""
    source_language: Annotated[PoLang, GetPydanticSchema(_po_lang_schema)]
    """The language of the source strings (``msgid``)."""
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
                for msgid, context in duplicates
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
