# Desktop Render Context

This document describes the data that `metaglot desktop render` provides to a user-provided [Liquid](https://shopify.github.io/liquid/) template when rendering freedesktop desktop entry files.

MetaGlot reads templates as UTF-8 and writes the rendered file as UTF-8 (without BOM) using the system's native line endings. This encoding is a built-in constraint of the tool and is not configurable. Desktop entry files are UTF-8 by definition, so no encoding declaration is needed (see the `example` folder for a complete sample).

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
| `locale` | string | The desktop entry locale of the language, used as the `LOCALE` postfix of localized keys, e.g. `en_US`, `zh_CN`, `sr_RS@latin`. |
| `strings` | mapping of string to string | Maps every manifest entry key to its resolved text, e.g. `lang.strings.name`. |

The resolved text of an entry falls back to the manifest source string when the entry is untranslated, missing from the PO file, or marked fuzzy.

The `locale` property holds the value defined by the desktop entry specification for localized keys: the language and country codes carry over from the PO language unchanged, and the Gettext variant slot fills the locale's modifier slot (e.g. `sr_RS@latin` stays `sr_RS@latin`). Every valid PO language converts successfully; there is no "unmapped language" rejection (unlike RC rendering).

## Default Object

The top-level `default` is a language object of the same shape as the entries of `languages`. It describes the manifest's source language (`source_language`) and is always present. It is built directly from the manifest's source strings — never from PO files — and is not part of the `languages` array: iterating `languages` yields the translation languages only.

The desktop entry specification requires every localized key (e.g. `Name[zh_CN]`) to be accompanied by the same key without a locale postfix (e.g. `Name`). `default.strings` is the intended source for those unlocalized keys:

```liquid
Name={{ default.strings.name | desktop_escape }}
```

## Filters

All filters described in [filters.md](filters.md) are available when rendering desktop entry files: the general filters available in every rendering, and the desktop filters such as `desktop_escape`.
