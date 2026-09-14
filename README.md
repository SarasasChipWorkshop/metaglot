# MetaGlot

<!--
"Meta" is coming from "metadata".
"Glot" is coming from "polyglot".
-->

**Platform Metadata Localization Compiler**

> One POT, all platforms.

MetaGlot is a command-line tool that unifies localization metadata for applications shipped on multiple platforms. It extracts or defines translatable strings from platform-specific metadata files, normalizes them into Gettext-compatible POT/PO catalogs, and compiles translated PO files back into platform-native files.

It currently is designed for projects that ship on:

- **Windows** using RC resource files
- **Linux** using `.desktop` and AppStream MetaInfo XML files
- **macOS** using `Info.plist` and localized `InfoPlist.strings` files

Instead of asking translators to edit platform-specific formats, MetaGlot lets them work with standard Gettext PO files.

## Why MetaGlot?

Every platform has its own localization mechanism for application metadata:

| Platform | Metadata format | Localization mechanism |
|---|---|---|
| Windows | `.rc` | String tables, version resources |
| Linux | `.desktop` | `Name`, `Comment`, etc. |
| Linux | AppStream XML | `<name>`, `<summary>`, `<description>` |
| macOS | `Info.plist` | `InfoPlist.strings`, plist keys |

These formats are necessary for packaging and distribution, but they are inconvenient as translation sources. MetaGlot introduces a common localization layer.

MetaGlot does not replace Gettext. It makes Gettext the canonical translation workflow for platform metadata.

## License

MetaGlot is released under the MIT License. See `LICENSE` for details.
