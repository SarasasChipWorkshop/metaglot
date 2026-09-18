# AppStream Render Context

This document describes the data that `metaglot render appstream` provides to a user-provided [Liquid](https://shopify.github.io/liquid/) template when rendering AppStream metainfo XML files.

MetaGlot reads templates as UTF-8 and writes the rendered file as UTF-8 (without BOM) using the system's native line endings. This encoding is a built-in constraint of the tool and is not configurable. AppStream XML files are UTF-8 by definition, so the XML declaration should say so (see the `example` folder for a complete sample).

The renderer runs in strict mode: referencing a variable or a property that does not exist fails the render.

## Top-Level Variables

| Variable | Type | Description |
|---|---|---|
| `languages` | array of language | One entry per translation language, see below. |
| `default` | language | The manifest's source language entry, see below. |

The order of the `languages` entries is not guaranteed: they appear in the order their PO files are matched. The manifest's source language is **not** merged into the array (unlike the RC rendering, which always synthesizes it): `languages` holds exactly the languages of the provided PO files, and the source language is exposed separately as the top-level `default` variable, built directly from the manifest's source strings without reading any PO file. If a PO file for the source language is provided, its language appears in the array as a regular entry alongside `default`.

The language of a PO file is resolved from its `Language:` header, falling back to the file name without extension; only values valid as Gettext `Language` fields are accepted. Two PO files describing the same language, and PO entries unknown to the manifest, are rejected.

## Language Object

| Property | Type | Description |
|---|---|---|
| `name` | string | The language tag of the PO file, e.g. `en_US`, `zh_CN`. |
| `lang` | string | The BCP 47 language tag for `xml:lang`, e.g. `en-US`, `zh-CN`, `sr-Latn-RS`, `ca-ES-valencia`. |
| `strings` | mapping of string to string | Maps every manifest entry key to its resolved text, e.g. `lang.strings.name`. |

The resolved text of an entry falls back to the manifest source string when the entry is untranslated, missing from the PO file, or marked fuzzy.

### Language Tag Conversion

The `lang` property holds a BCP 47 language tag, as required by the `xml:lang` attribute: the language and country codes of the PO language carry over unchanged, hyphenated. The Gettext variant slot fills either the script subtag or the variant subtag, whichever interpretation the variant word supports: known script words (`latin`, `cyrillic`, `arabic`) become script subtags placed before the country (`sr_RS@latin` becomes `sr-Latn-RS`), while other words become variant subtags placed after it (`ca_ES@valencia` becomes `ca-ES-valencia`).

Tags are validated against BCP 47 with the IANA subtag registry: legacy Gettext variants that are not registered there (e.g. `euro`) are rejected with an error instead of being emitted as invalid `xml:lang` values. The conversion never rewrites a tag beyond hyphenation: no script is injected or removed, and no macrolanguage folding happens, so an emitted `xml:lang` is always a faithful hyphenation of its Gettext source tag.

## Default Object

The top-level `default` is a language object of the same shape as the entries of `languages`. It describes the manifest's source language (`source_language`) and is always present. It is built directly from the manifest's source strings — never from PO files — and is not part of the `languages` array: iterating `languages` yields the translation languages only.

AppStream uses the element without `xml:lang` as the untranslated default, mirroring how desktop entry files use unlocalized keys. `default.strings` is the intended source for those elements:

```liquid
<name>{{ default.strings.name | xml_escape }}</name>
```

## Filters

All filters described in [filters.md](filters.md) are available when rendering AppStream XML files: the general filters available in every rendering, and the AppStream filters such as `xml_escape`. Note that translated descriptions may legitimately carry AppStream markup (e.g. `<em>`); such values must not be passed through `xml_escape`, and deciding what to escape is the template author's responsibility.
