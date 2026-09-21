# Plist Render Context

This document describes the data that `metaglot render plist` provides to user-provided [Liquid](https://shopify.github.io/liquid/) templates when rendering macOS bundle metadata files.

Like the MSIX rendering, a plist rendering involves multiple output files: one `Info.plist` carrying the source-language metadata, plus one `InfoPlist.strings` file per language under a language-tagged folder (typically `Contents/Resources/<lang>.lproj/InfoPlist.strings`). Unlike the MSIX manifest, `Info.plist` carries no resource references: it writes the source strings directly, while every localized value lives in the `InfoPlist.strings` files. The output location of every file is resolved by a path template command line argument instead of a fixed output file argument.

MetaGlot reads templates as UTF-8 and writes every rendered file as UTF-8 (without BOM) using the system's native line endings. This encoding is a built-in constraint of the tool and is not configurable. The renderer runs in strict mode: referencing a variable or a property that does not exist fails the render.

Every component below renders with its **own environment**, so the filters available to one component never leak into another. Path templates resolve to paths relative to the output folder (an absolute rendered path is used as-is); their result is stripped of surrounding whitespace and must not be empty.

## Path Template Contexts

The `--plist-path` and `--strings-path` arguments are in-memory Liquid templates rendered into output paths. Only the general filters described in [filters.md](../filters.md) are available to them.

### `--plist-path`

| Variable | Type | Description |
|---|---|---|
| (none) | | The context is empty: the path is typically the plain literal `Contents/Info.plist`. |

The template is rendered once. Referencing any variable fails the render.

### `--strings-path`

| Variable | Type | Description |
|---|---|---|
| `lang` | string | The BCP 47 language tag of the InfoPlist.strings file being placed, e.g. `en`, `zh-Hans`, `sr-Latn-RS`. |

The template is rendered once per language, for example:

```liquid
Contents/Resources/{{ lang }}.lproj/InfoPlist.strings
```

## File Render Contexts

The `--plist-template` and `--strings-template` arguments point to template files. Besides the general filters, the Info.plist rendering provides `xml_escape`, and the InfoPlist.strings rendering provides `plist_strings_escape`.

### `--plist-template`

| Variable | Type | Description |
|---|---|---|
| `default` | language | The manifest's source language entry, see below. |
| `langs` | array of string | The BCP 47 language tag of every language, source language first. |

`Info.plist` writes the source strings directly through `default`:

```liquid
<key>CFBundleDisplayName</key>
<string>{{ default.strings.app_display_name | xml_escape }}</string>
```

`langs` lists every language that gets an InfoPlist.strings file, useful for enumerating `CFBundleLocalizations`:

```xml
<key>CFBundleLocalizations</key>
<array>
{% for lang in langs %}
  <string>{{ lang }}</string>
{% endfor %}
</array>
```

The source language always leads `langs` and always gets an InfoPlist.strings file: it comes from a PO file when one provides it, and is otherwise synthesized from the manifest's source strings. Every language listed in `langs` is guaranteed a complete `.lproj` folder.

### `--strings-template`

The members of the current language are exposed at the top level. The structure is identical for every language; only the data differs. There is no `default`.

| Variable | Type | Description |
|---|---|---|
| `name` | string | The language tag of the PO file, e.g. `en_US`, `zh_CN`. |
| `lang` | string | The BCP 47 language tag of this InfoPlist.strings file, e.g. `en`, `zh-Hans-CN`, `sr-Latn-RS`. |
| `strings` | mapping of string to string | Maps every manifest entry key to its resolved text, e.g. `strings.app_display_name`. |
| `sources` | mapping of string to string | Maps every manifest entry key to its manifest source text, e.g. `sources.file_type_jpeg`. |

The resolved text of an entry falls back to the manifest source string when the entry is untranslated, missing from the PO file, or marked fuzzy. The template is rendered once per language.

`InfoPlist.strings` entries use two key forms, and `sources` exists because of the second one:

- Top-level `Info.plist` values (`CFBundleDisplayName`, `NSHumanReadableCopyright`, the `NS*UsageDescription` keys, ...) are localized with the **Info.plist key name** as the key.
- Nested display values inside arrays (`CFBundleTypeName` of a document type, `UTTypeDescription` of an exported UTI, `CFBundleURLName` of a URL scheme) are localized with their **source text** as the key. One entry keyed by the source text localizes every field sharing that text:

```liquid
"CFBundleDisplayName" = "{{ strings.app_display_name | plist_strings_escape }}";
"{{ sources.file_type_jpeg | plist_strings_escape }}" = "{{ strings.file_type_jpeg | plist_strings_escape }}";
```

The `lang` conversion follows BCP 47 with the shared composition rules: the language and country codes carry over hyphenated, known script words (`latin`, `cyrillic`, `arabic`) become script subtags placed before the country (`sr_RS@latin` becomes `sr-Latn-RS`), and other variant words become variant subtags after it. Legacy Gettext variants that the IANA registry does not register (e.g. `euro`) are rejected.
