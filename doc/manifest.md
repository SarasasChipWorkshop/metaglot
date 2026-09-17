# String Manifest

This document describes how to write a MetaGlot string manifest: the TOML file that declares the translatable strings of an application's metadata.

The manifest is platform-neutral. It only describes *what* can be translated, not how translations end up in any particular platform format; MetaGlot reads it to produce Gettext translation catalogs and to fill platform-native output files. The file must be encoded in UTF-8.

## Top-Level Fields

| Field | Type | Description |
|---|---|---|
| `version` | int | The manifest format version. Currently `1`; any other value is rejected. |
| `strings` | table | All translatable strings. Each item maps a string entry key to a string entry, see below. |

## String Entry

| Field | Type | Description |
|---|---|---|
| `msgid` | string | Required. The untranslated source string. |
| `context` | string | Optional. Disambiguates entries that share the same `msgid` but are used differently, mirroring the context (`msgctxt`) mechanism of Gettext. Defaults to empty. |
| `comment` | string | Optional. A note for translators explaining where and how the string is used. Defaults to empty. |

The string entry key identifies the entry inside the manifest and in generated outputs. It must be non-empty; both numeric IDs (e.g. `1000`) and names (e.g. `file_description`) are acceptable, and numeric IDs are represented as strings.

## Validation Rules

A manifest is rejected when:

- `version` is not matched with current value introduced above.
- Any string entry key is empty.
- Two entries share both `msgid` and `context`.
- An entry or the document root contains unknown fields.

## Example

```toml
version = 1

[strings.panel_title]
msgid = "Example - Image Viewer"
context = "Explorer"
comment = "Shown by the file manager in the properties panel."

[strings.file_type_jpeg]
msgid = "JPEG Image"
comment = "File type name for: jpg, jpeg, jfif"

[strings.file_type_png]
msgid = "PNG Image"
comment = "File type name for: png"

[strings.file_description]
msgid = "Example - Image Viewer"
context = "Self"
comment = "File description of the executable."

[strings.product_name]
msgid = "Example"
comment = "Display name of the product."
```

Note that entries `panel_title` and `file_description` share the same `msgid`. This is allowed because their `context` values differ; without distinct contexts the combination would be rejected as ambiguous.
