# Liquid Filters

MetaGlot renders output files through [Liquid](https://shopify.github.io/liquid/) templates. The filters MetaGlot provides are grouped by rendering target and described in this document.

The rendering environment runs in strict mode: referencing a variable or a property that does not exist fails the render.

## General Filters

The following filters are available in every rendering.

| Filter | Description |
|---|---|
| `to_string` | Convert the value to its string representation. |
| `format` | Treat the value as a Python format template and apply `str.format` with the arguments passed to the filter. |
| `to_integer` | Convert the value to an integer. |
| `to_float` | Convert the value to a float. |
| `is_integer` | Whether the value can be parsed as an integer. |
| `is_float` | Whether the value can be parsed as a float. |

Examples:

```liquid
{{ 1000 | to_string }}          {% comment %}renders "1000"{% endcomment %}
{{ "ID: {0}" | format: 1001 }}  {% comment %}renders "ID: 1001"{% endcomment %}
```

## RC Filters

The following filters are available only when rendering Windows RC files.

| Filter | Description |
|---|---|
| `rc_escape` | Escapes a string for use inside a double-quoted C-style string literal, such as an RC string table entry: `\` becomes `\\` and `"` becomes `\"`. |

## Desktop Filters

The following filters are available only when rendering desktop entry files.

| Filter | Description |
|---|---|
| `desktop_escape` | Escapes a string for use as a desktop entry `string`, `localestring` or `iconstring` value: `\` becomes `\\`, newline becomes `\n`, carriage return becomes `\r` and tab becomes `\t` anywhere; leading and trailing spaces become `\s`. Semicolons are not escaped, because they separate the values of plural keys (e.g. `Keywords`); escape them with the standard `replace` filter when composing such values item by item. |

## AppStream Filters

The following filters are available only when rendering AppStream XML files.

| Filter | Description |
|---|---|
| `xml_escape` | Escapes a string for use in XML text content or attribute values: `&` becomes `&amp;`, `<` becomes `&lt;`, `>` becomes `&gt;`, `"` becomes `&quot;` and `'` becomes `&apos;`. Values that intentionally carry AppStream markup (e.g. `<em>` inside descriptions) must not be passed through this filter; whether to escape is the template author's decision. |

Examples:

```liquid
{{ "Example" | xml_escape }}  {% comment %}renders "Example"{% endcomment %}
```

Examples:

```liquid
{{ "Example" | desktop_escape }}  {% comment %}renders "Example"{% endcomment %}
```

## MSIX Filters

The following filters are available when rendering MSIX files. `xml_escape` is available to the manifest file rendering; both filters are available to the resources file rendering, where the template decides between a `.resw` (XML) and a `.resjson` (JSON) output.

| Filter | Available to | Description |
|---|---|---|
| `xml_escape` | manifest, resources | The same filter described in the AppStream section above; `AppxManifest.xml` and `.resw` files are XML too. |
| `json_escape` | resources | Escapes a string for use inside a JSON string literal, such as a `.resjson` value: `\` becomes `\\`, `"` becomes `\"`, newline, carriage return and tab become `\n`, `\r` and `\t`, and any other control character below 0x20 becomes its `\uXXXX` form. Like the other escape filters it adds no surrounding quotes; write them in the template: `"{{ strings.key \| json_escape }}"`. |

Examples:

```liquid
{{ "Example" | json_escape }}  {% comment %}renders "Example", without quotes{% endcomment %}
```
