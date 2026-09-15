# RC Render Context

This document describes the data that `metaglot rc render` provides to a user-provided
[Liquid](https://shopify.github.io/liquid/) template when rendering Windows RC files.

MetaGlot reads templates as UTF-8 and writes the rendered file as UTF-8 (without BOM)
using the system's native line endings. This encoding is a built-in constraint of the
tool and is not configurable. Because the generated file is UTF-8, templates should
declare the encoding with `#pragma code_page(65001)` so that the RC compiler parses
the file correctly (see the `example` folder for a complete sample).

The renderer runs in strict mode: referencing a variable or a property that does not
exist fails the render.

## Top-level variables

| Variable    | Type              | Description |
|-------------|-------------------|-------------|
| `languages` | array of language | One entry per language, see below. |

The order of the entries is not guaranteed: they appear in the order their PO files
are matched. The presence of an English entry is not guaranteed either. An English
entry exists only if an English PO file is provided; otherwise it is simply absent,
and templates must handle that themselves (the text of every entry already falls
back to the manifest source string, which is typically English).

The language of a PO file is resolved from its `Language:` header, falling back to
the file name without extension; only values valid as Gettext `Language` fields are
accepted. Languages without a Windows language mapping, two PO files describing the
same language, and PO entries unknown to the manifest are rejected.

## Language object

| Property      | Type   | Description |
|---------------|--------|-------------|
| `name`        | string | Human-readable language name, e.g. `English (United States)`. |
| `langid`      | string | Windows language identifier in hexadecimal, e.g. `0x409`. |
| `primary`     | string | Windows primary language identifier in hexadecimal, e.g. `0x09`. |
| `sublanguage` | string | Windows sublanguage identifier in hexadecimal, e.g. `0x01`. |
| `block_key`   | string | Eight hex digits combining `langid` and the Unicode code page, suitable as a `StringFileInfo` block key, e.g. `040904B0`. |
| `code_page`   | string | The version resource code page in decimal, always `1200` (Unicode, `0x04B0`). It is fixed by MetaGlot's UTF-8 read/write pipeline and shares its source with `block_key`; templates must not attempt to use another code page. |
| `strings`     | mapping of string to string | Maps every manifest entry key to its resolved text, e.g. `lang.strings.file_description`. |

The resolved text of an entry falls back to the manifest source string when the
entry is untranslated, missing from the PO file, or marked fuzzy.

## Filters

All filters described in [filters.md](filters.md) are available when rendering RC
files: the general filters available in every rendering, and the RC filters such
as `rc_escape`.
