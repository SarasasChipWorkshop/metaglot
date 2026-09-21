# Examples

This folder holds one example per supported metadata type. Two kinds of files appear here:

- `.toml` files are string manifests: they declare the translatable strings of one metadata type.
- `.liquid` files are render templates: they decide how the translated strings are written back into the platform-native file.

## Windows RC Resource File

- `example.rc.toml` — The string manifest of the RC example.
- `example.rc.liquid` — Renders the `.rc` file, including string tables and version information blocks.

## Windows MSIX Package

- `AppxManifest.xml.toml` — The string manifest of the MSIX example.
- `AppxManifest.xml.liquid` — Renders the `AppxManifest.xml` package manifest, including the resource language list.
- `Resources.resw.liquid`, `Resources.resjson.liquid` — Render the per-language resources file. They hold the same content in the two accepted resource formats; pick whichever matches the packaging pipeline.

## Windows InnoSetup Script

- `example.iss.toml` — The string manifest of the InnoSetup example.
- `example.iss.liquid` — Renders the `.iss` installation script, including its `[Languages]` section.
- `example.isl.liquid` — Renders the per-language `.isl` messages files.

## Linux Desktop Entry

- `example.desktop.toml` — The string manifest of the desktop entry example.
- `example.desktop.liquid` — Renders the `.desktop` file, including localized keys such as `Name[zh_CN]`.

## Linux AppStream Metadata

- `example.metainfo.xml.toml` — The string manifest of the AppStream example.
- `example.metainfo.xml.liquid` — Renders the `.metainfo.xml` file, including translations marked with `xml:lang`.

## macOS Bundle

- `Info.plist.toml` — The string manifest of the macOS bundle example.
- `Info.plist.liquid` — Renders the bundle `Info.plist`.
- `InfoPlist.strings.liquid` — Renders the per-language `InfoPlist.strings` localization files.
