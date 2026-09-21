# Inno Render Context

This document describes the data that `metaglot render inno` provides to user-provided [Liquid](https://shopify.github.io/liquid/) templates when rendering Inno Setup installation files.

Like the MSIX and plist renderings, an Inno rendering involves multiple output files: one `.iss` script referencing localized custom messages through `{cm:...}` constants, plus one incremental `.isl` messages file per language carrying the `[CustomMessages]` entries. The output location of every file is resolved by a path template command line argument instead of a fixed output file argument.

MetaGlot reads templates as UTF-8 and writes every rendered file as UTF-8 (without BOM) using the system's native line endings. Inno Setup 6.3 and later recommend exactly this encoding for `.iss` and `.isl` files, so the output is used as-is. The renderer runs in strict mode: referencing a variable or a property that does not exist fails the render.

Every component below renders with its **own environment**, so the filters available to one component never leak into another. Path templates resolve to paths relative to the output folder (an absolute rendered path is used as-is); their result is stripped of surrounding whitespace and must not be empty.

## Language Identification

Inno Setup has **no standard representation of language identifiers**: the `[Languages]` internal `Name:` and the message file names are both chosen freely by the packager. MetaGlot therefore performs **no conversion** for this target - the PO language tag (`zh_CN`, `en`) carries over verbatim, and the same tag serves as the single join key across everything the pipeline generates:

- the `Name:` value of a `[Languages]` entry,
- the incremental `.isl` file name (e.g. `Strings\zh_CN.isl`),
- and the matching branch of the base file pairing in the `.iss` template (see below).

The pairing between a language and its base `.isl` - the official full translation whose `[LangOptions]` provides the language identity (the Select Language dialog name and the auto-detection identifier) - is knowledge of the template author and is expressed explicitly, for example:

```liquid
{% for lang in langs %}
{% case lang %}
{% when 'zh_CN' %}
{% assign base = 'compiler:Languages\ChineseSimplified.isl' %}
{% when 'ja' %}
{% assign base = 'compiler:Languages\Japanese.isl' %}
{% else %}
{% assign base = 'compiler:Default.isl' %}
{% endcase %}
Name: "{{ lang }}"; MessagesFile: "{{ base }},Strings\{{ lang }}.isl"
{% endfor %}
```

The multi-line decision block renders some blank lines into the INI output, which is harmless; Liquid's whitespace control markers (`{%-`/`-%}`) can remove them once used consistently across templates.

Keep the `case` branches aligned with the languages you ship PO files for: an unmatched language falls to the `{% else %}` base (usually `compiler:Default.isl`) and inherits the English language identity. Review the rendered `[Languages]` section after adding a new language.

## Path Template Contexts

The `--iss-path` and `--isl-path` arguments are in-memory Liquid templates rendered into output paths. Only the general filters described in [filters.md](filters.md) are available to them.

### `--iss-path`

| Variable | Type | Description |
|---|---|---|
| (none) | | The context is empty: the path is typically the plain literal `example.iss`. |

The template is rendered once. Referencing any variable fails the render.

### `--isl-path`

| Variable | Type | Description |
|---|---|---|
| `lang` | string | The PO language tag of the `.isl` messages file being placed, e.g. `en`, `zh_CN`. |

The template is rendered once per language, for example:

```liquid
Strings/{{ lang }}.isl
```

## File Render Contexts

The `--iss-template` and `--isl-template` arguments point to template files. Besides the general filters, the Inno filter (`inno_escape`) is available to both.

### `--iss-template`

| Variable | Type | Description |
|---|---|---|
| `default` | language | The manifest's source language entry, see below. |
| `langs` | array of string | The PO language tag of every language, source language first. |

The `.iss` script references the localized text through `{cm:...}` constants (e.g. `AppName={cm:app_name}`) and enumerates `[Languages]` from `langs` with the base file pairing shown above. `default` is available for values written directly instead of via constants:

```liquid
AppName={{ default.strings.app_name | inno_escape }}
```

The source language always leads `langs` and always gets an `.isl` messages file: it comes from a PO file when one provides it, and is otherwise synthesized from the manifest's source strings.

### `--isl-template`

The members of the current language are exposed at the top level. The structure is identical for every language; only the data differs. There is no `default`.

| Variable | Type | Description |
|---|---|---|
| `name` | string | The PO language tag of this `.isl` messages file, e.g. `en_US`, `zh_CN`. |
| `strings` | mapping of string to string | Maps every manifest entry key to its resolved text, e.g. `strings.app_name`. |

The resolved text of an entry falls back to the manifest source string when the entry is untranslated, missing from the PO file, or marked fuzzy. The template is rendered once per language.

The recommended shape of a generated `.isl` is a plain `[CustomMessages]` section: language identity (the `[LangOptions]` fields) is inherited from the base `.isl` listed before it in `MessagesFile`, following the merge order of Inno Setup.

```liquid
[CustomMessages]
app_name={{ strings.app_name | inno_escape }}
```
