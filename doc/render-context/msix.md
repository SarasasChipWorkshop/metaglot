# MSIX Render Context

This document describes the data that `metaglot render msix` provides to user-provided [Liquid](https://shopify.github.io/liquid/) templates when rendering Windows MSIX files.

Unlike the other targets, an MSIX rendering involves multiple output files: one `AppxManifest.xml` (or `Package.appxmanifest`) referencing localized strings through `ms-resource:` URIs, plus one `Resources.resw` or `Resources.resjson` file per language under a language-tagged folder (typically `Strings/<lang>/Resources.resw`). The output location of every file is resolved by a path template command line argument instead of a fixed output file argument.

MetaGlot reads templates as UTF-8 and writes every rendered file as UTF-8 (without BOM) using the system's native line endings. This encoding is a built-in constraint of the tool and is not configurable. The renderer runs in strict mode: referencing a variable or a property that does not exist fails the render.

Every component below renders with its **own environment**, so the filters available to one component never leak into another. Path templates resolve to paths relative to the output folder (an absolute rendered path is used as-is); their result is stripped of surrounding whitespace and must not be empty.

## Path Template Contexts

The `--manifest-path` and `--resources-path` arguments are in-memory Liquid templates rendered into output paths. Only the general filters described in [filters.md](../filters.md) are available to them.

### `--manifest-path`

| Variable | Type | Description |
|---|---|---|
| (none) | | The context is empty: the path is typically the plain literal `AppxManifest.xml`. |

The template is rendered once. Referencing any variable fails the render.

### `--resources-path`

| Variable | Type | Description |
|---|---|---|
| `lang` | string | The BCP 47 language tag of the resources file being placed, e.g. `en-US`, `zh-CN`. |

The template is rendered once per language, for example:

```liquid
Strings/{{ lang }}/Resources.resw
```

## File Render Contexts

The `--manifest-template` and `--resources-template` arguments point to template files. Besides the general filters, the manifest template rendering provides `xml_escape`, and the resources template rendering provides `xml_escape` and `json_escape`.

### `--manifest-template`

| Variable | Type | Description |
|---|---|---|
| `default` | language | The manifest's source language entry, see below. |
| `langs` | array of string | The BCP 47 language tag of every language, source language first. |

The manifest itself carries no translated text: it references resources through `ms-resource:` URIs and lists every language for the `<Resources>` section, where the first listed language acts as the default one:

```xml
<Resources>
{% for lang in langs %}
  <Resource Language="{{ lang }}" />
{% endfor %}
</Resources>
```

`default` is provided for manifests that opt out of localization and write text directly: `{{ default.strings.app_display_name | xml_escape }}`. A fully localized manifest instead writes `ms-resource:AppDisplayName` and friends.

The source language always leads `langs` and always gets a resources file: it comes from a PO file when one provides it, and is otherwise synthesized from the manifest's source strings. Every language listed in `langs` is guaranteed a complete resources folder, since any language may become a user's fallback.

### `--resources-template`

The members of the current language are exposed at the top level. The structure is identical for every language; only the data differs. There is no `default`.

| Variable | Type | Description |
|---|---|---|
| `name` | string | The language tag of the PO file, e.g. `en_US`, `zh_CN`. |
| `lang` | string | The BCP 47 language tag of this resources file, e.g. `en-US`, `zh-CN`, `sr-Latn-RS`. |
| `strings` | mapping of string to string | Maps every manifest entry key to its resolved text, e.g. `strings.app_display_name`. |

The resolved text of an entry falls back to the manifest source string when the entry is untranslated, missing from the PO file, or marked fuzzy. The template is rendered once per language:

```liquid
{
  "AppDisplayName": "{{ strings.app_display_name | json_escape }}"
}
```

The `lang` conversion follows BCP 47 with the shared composition rules: the language and country codes carry over hyphenated, known script words (`latin`, `cyrillic`, `arabic`) become script subtags placed before the country (`sr_RS@latin` becomes `sr-Latn-RS`), and other variant words become variant subtags after it. Legacy Gettext variants that the IANA registry does not register (e.g. `euro`) are rejected.
