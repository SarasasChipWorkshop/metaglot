# Liquid Filters

MetaGlot renders output files through [Liquid](https://shopify.github.io/liquid/)
templates. The filters MetaGlot provides are grouped by rendering target and
described in this document.

The rendering environment runs in strict mode: referencing a variable or a property
that does not exist fails the render.

## General filters

The following filters are available in every rendering.

| Filter       | Description |
|--------------|-------------|
| `to_string`  | Convert the value to its string representation. |
| `format`     | Treat the value as a Python format template and apply `str.format` with the arguments passed to the filter. |
| `to_integer` | Convert the value to an integer. |
| `to_float`   | Convert the value to a float. |
| `is_integer` | Whether the value can be parsed as an integer. |
| `is_float`   | Whether the value can be parsed as a float. |

Examples:

```liquid
{{ 1000 | to_string }}          {% comment %}renders "1000"{% endcomment %}
{{ "ID: {0}" | format: 1001 }}  {% comment %}renders "ID: 1001"{% endcomment %}
```

## RC filters

The following filters are available only when rendering Windows RC files.

| Filter      | Description |
|-------------|-------------|
| `rc_escape` | Escapes a string for use inside a double-quoted C-style string literal, such as an RC string table entry: `\` becomes `\\` and `"` becomes `\"`. |
