# Inno Render Context

This document describes the data that `metaglot render inno` provides to user-provided [Liquid](https://shopify.github.io/liquid/) templates when rendering Inno Setup installation files.

Like the MSIX and plist renderings, an Inno rendering involves multiple output files: one `.iss` script referencing localized custom messages through `{cm:...}` constants, plus one incremental `.isl` messages file per language carrying the `[CustomMessages]` entries. The output location of every file is resolved by a path template command line argument instead of a fixed output file argument.

MetaGlot reads templates as UTF-8 and writes every rendered file as UTF-8 (without BOM) using the system's native line endings. Inno Setup 6.3 and later recommend exactly this encoding for `.iss` and `.isl` files, so the output is used as-is. The renderer runs in strict mode: referencing a variable or a property that does not exist fails the render.

Every component below renders with its **own environment**, so the filters available to one component never leak into another. Path templates resolve to paths relative to the output folder (an absolute rendered path is used as-is); their result is stripped of surrounding whitespace and must not be empty.

## Language Identification

Inno Setup has **no standard representation of language identifiers**: the `[Languages]` internal `Name:` and the message file names are both chosen freely by the packager. What does exist is a set of **conventional file names** — the base names of the messages files distributed by the Inno Setup project itself, such as `ChineseSimplified` or `Japanese`.

MetaGlot therefore exposes **two** language identifiers and **one** provenance flag per language:

- `name` — the PO language tag (`zh_CN`, `en`), carried over verbatim. It is the canonical join key across everything the pipeline generates: the `Name:` value of a `[Languages]` entry, the language ordering, and the fallback identifier when the conversion below fails.
- `lang` — the best-effort conversion of the PO tag to a conventional Inno Setup language name (`zh_CN` → `ChineseSimplified`, `ja`/`ja_JP` → `Japanese`). It is `null` when no conventional name is known for the language; handle those languages with `{{ lang | default: name }}`, or with a `case`/`when` block on `name`.
- `is_official` — whether `lang` belongs to a translation bundled with the **targeted** Inno Setup version, as given by the required `--inno-version` command line option (`true`), or not (`false`). It is also `false` when `lang` is `null`, since there is no official file to reference then. Only the bundled files come with an Inno Setup installation; the others must be downloaded from the [translations page](https://jrsoftware.org/files/istrans/) and shipped with the installer yourself. Do **not** pair such a language with `compiler:Default.isl` as a fallback — drop it instead, as shown below.

The conversion table transcribes the conventional names from the [unofficial translations page](https://jrsoftware.org/files/istrans/) — official and community lists alike, including the outdated ones — so adding a new language with a known name requires no template edits. Country-sensitive languages are disambiguated: `zh`/`zh_SG` → `ChineseSimplified` but `zh_TW`/`zh_HK`/`zh_MO` → `ChineseTraditional`; `pt` → `Portuguese` but `pt_BR` → `BrazilianPortuguese`; `en` → `Default` but `en_GB` → `EnglishBritish`; `no`/`nb` → `Norwegian` but `nn` → `NorwegianNynorsk`; `sr` → `SerbianCyrillic` but `sr_RS@latin` → `SerbianLatin`; `ca_ES@valencia` → `Valencian`.

The officiality behind `is_official` is transcribed from the `Languages` folder listings of Inno Setup **6.7.1** and **7.1.0**. The two differ in four names: `ChineseSimplified`, `ChineseTraditional`, `Lithuanian` and `Thai` are bundled with Inno Setup 7 only, so they count as official solely when `--inno-version 7` is given. `Icelandic` is listed as an official translation by the translations page, but neither listing ships it, so it is never official.

Caveats:

- English has no dedicated file: `en` converts to `Default`, because `Default.isl` lives at the compiler root instead of the `Languages` subfolder.
- `Default.isl` is not a neutral fallback base: every `[Languages]` entry inherits the language identity of its base file (the `[LangOptions]` `LanguageName` and `LanguageID`, which drive the Select Language dialog and the default language detection), and `Default.isl` carries the English identity. Pairing fallback entries with it floods the dialog with duplicate English items, so languages without a usable base file are dropped instead.
- The converted name is the file **base name** (`ChineseSimplified`), not the `LanguageName` field inside the file (`Chinese (Simplified)`).
- Seven legacy community files ship with a `.islu` extension (Bengali, Hindi, Kazakh, Marathi, Nepali, Sinhala, Uyghur); the conversion returns base names only, and the extension is the template author's concern.
- Outdated community files predate the current Inno Setup message set; they still load, but their missing messages fall back to English.

With the conversion available, the base file pairing between a language and its base `.isl` — the official full translation whose `[LangOptions]` provides the language identity (the Select Language dialog name and the auto-detection identifier) — keeps one special case, the location of `Default.isl`, plus a drop rule for everything without an official base file:

```liquid
{% for lang in langs -%}
{%- if lang.is_official -%}
{%- if lang.lang == 'Default' -%}
{% assign base = 'compiler:Default.isl' -%}
{%- else -%}
{% assign base = 'compiler:Languages\' | append: lang.lang | append: '.isl' -%}
{%- endif -%}
Name: "{{ lang.name }}"; MessagesFile: "{{ base }},Strings\{{ lang.lang }}.isl"
{% else -%}
{%- comment -%}
unofficial or unmapped: dropped, since a Default.isl fallback would duplicate the English identity in the Select Language dialog
{%- endcomment -%}
{% endif -%}
{% endfor -%}
```

The `else` branch emits nothing: languages whose `lang` is `null` or not official are dropped from the `[Languages]` section, so the Select Language dialog stays free of duplicate English entries. Note that dropping happens only in the `.iss` template; the `.isl` rendering loop is independent and still writes a messages file for every language (see the note under `--isl-path`). If you want to keep a community localization, download its `.isl` from the translations page, ship it next to your installer, and widen the branch condition to pair it explicitly. Review the rendered `[Languages]` section after adding a new language.

The whitespace control markers (`{%-`/`-%}`) keep the decision block from rendering blank lines into the INI output; use them consistently across the block.

## Path Template Contexts

The `--iss-path` and `--isl-path` arguments are in-memory Liquid templates rendered into output paths. Only the general filters described in [filters.md](../filters.md) are available to them.

### `--iss-path`

| Variable | Type | Description |
|---|---|---|
| (none) | | The context is empty: the path is typically the plain literal `example.iss`. |

The template is rendered once. Referencing any variable fails the render.

### `--isl-path`

| Variable | Type | Description |
|---|---|---|
| `lang` | string or null | The conventional Inno Setup language name of the `.isl` messages file being placed, e.g. `ChineseSimplified`; `null` when no conventional name exists. |
| `name` | string | The PO language tag of the `.isl` messages file being placed, e.g. `en`, `zh_CN`. |
| `is_official` | boolean | Whether the conventional name is bundled with the Inno Setup version targeted by `--inno-version`; `false` otherwise and when `lang` is `null`. |

The template is rendered once per language, for example:

```liquid
Strings/{{ lang | default: name }}.isl
```

The rendering loop is independent of the dropping decision in the `.iss` template: a language dropped from `[Languages]` still gets its `.isl` messages file written, unreferenced by the installation script. Delete such leftovers in your packaging step if unwanted.

## File Render Contexts

The `--iss-template` and `--isl-template` arguments point to template files. Besides the general filters, the Inno filter (`inno_escape`) is available to both.

### `--iss-template`

| Variable | Type | Description |
|---|---|---|
| `default` | language | The manifest's source language entry, see below. |
| `langs` | array of language | Every language, source language first. Each entry exposes `name` (the PO language tag), `lang` (the conventional Inno Setup language name, or null) and `is_official` (whether the name is bundled with the Inno Setup version targeted by `--inno-version`). |

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
| `lang` | string or null | The conventional Inno Setup language name of this `.isl` messages file, e.g. `Japanese`; `null` when no conventional name exists. |
| `is_official` | boolean | Whether the conventional name is bundled with the Inno Setup version targeted by `--inno-version`; `false` otherwise and when `lang` is `null`. |
| `strings` | mapping of string to string | Maps every manifest entry key to its resolved text, e.g. `strings.app_name`. |

The resolved text of an entry falls back to the manifest source string when the entry is untranslated, missing from the PO file, or marked fuzzy. The template is rendered once per language.

The recommended shape of a generated `.isl` is a plain `[CustomMessages]` section: language identity (the `[LangOptions]` fields) is inherited from the base `.isl` listed before it in `MessagesFile`, following the merge order of Inno Setup.

```liquid
[CustomMessages]
app_name={{ strings.app_name | inno_escape }}
```
