# RC Render Context

This document describes the data that `metaglot rc render` provides to a user-provided
[Liquid](https://shopify.github.io/liquid/) template when rendering Windows RC files.

The renderer runs in strict mode: referencing a variable or a property that does not
exist fails the render. Output is written as UTF-8 (without BOM) using LF line endings.

## Top-level variables

| Variable    | Type              | Description |
|-------------|-------------------|-------------|
| `languages` | array of language | One entry per language, see below. The English (`en`) entry is always present and comes first; remaining entries follow in the order their PO files are matched. |

## Language object

| Property      | Type   | Description |
|---------------|--------|-------------|
| `name`        | string | Human-readable language name, e.g. `English (United States)`. |
| `locale`      | string | Gettext-style locale code, e.g. `en`, `zh_CN`. |
| `langid`      | string | Windows language identifier in hexadecimal, e.g. `0x409`. |
| `primary`     | string | Windows primary language identifier in hexadecimal, e.g. `0x09`. |
| `sublanguage` | string | Windows sublanguage identifier in hexadecimal, e.g. `0x01`. |
| `block_key`   | string | Eight hex digits combining `langid` and code page 1200 (`0x4B0`), suitable as a `StringFileInfo` block key, e.g. `040904B0`. |
| `strings`     | array of string entry | All manifest entries, in manifest order, see below. |
| `named`       | mapping of string to string | Maps every entry key to its translated text, convenient for direct access such as `lang.named.file_description`. |

The locale of a PO file is resolved from its `Language:` header, falling back to the
file name without extension. Locales without a Windows language mapping are rejected.

## String entry object

| Property  | Type   | Description |
|-----------|--------|-------------|
| `key`     | string | The entry key from the manifest, e.g. `100` or `file_description`. Numeric resource IDs are represented as strings. |
| `msgid`   | string | The untranslated source string. |
| `text`    | string | The translated text for this language. Falls back to `msgid` when the entry is untranslated or marked fuzzy. Provided raw, without any escaping. |
| `context` | string | The entry context from the manifest, e.g. `File type name for: jpg, jpeg, jfif`. |

## Filters

| Filter      | Description |
|-------------|-------------|
| `rc_escape` | Escapes a string for use inside a double-quoted RC string literal: `\` becomes `\\` and `"` becomes `\"`. |
