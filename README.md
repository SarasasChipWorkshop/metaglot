# MetaGlot

<!--
"Meta" is coming from "metadata".
"Glot" is coming from "polyglot".
-->

**Platform Metadata Localization Compiler**

> One POT, all platforms.

MetaGlot is a command-line tool that unifies localization metadata for applications shipped on multiple platforms. It extracts or defines translatable strings from platform-specific metadata files, normalizes them into Gettext-compatible POT/PO catalogs, and compiles translated PO files back into platform-native files.

It currently is designed for projects that ship on Windows, Linux and macOS.

Instead of asking translators to edit platform-specific formats, MetaGlot lets them work with standard Gettext PO files.

## Why MetaGlot?

Every platform has its own localization mechanism for application metadata. Windows applications use RC resource files to hold string tables and version resources, Linux applications use `.desktop` files to describe names and comments, and macOS applications use `Info.plist` together with localized `InfoPlist.strings` files.

These formats are necessary for packaging and distribution, but they are inconvenient as translation sources. MetaGlot introduces a common localization layer.

MetaGlot does not replace Gettext. It makes Gettext the canonical translation workflow for platform metadata.

## Supported Metadata Types

MetaGlot supports compiling metadata from the following formats:

| Platform | Metadata format |
|---|---|
| Windows | Windows reosurce file `.rc` |
| Windows | MSIX manifest (`Package.appxmanifest` or `AppxManifest.xml`) and localization files (`.resw` or `.resjson`) |
| Windows | InnoSetup script (`.iss`) and its localization files (`.isl`) |
| Linux | `.desktop` file |
| Linux | AppStream XML file (`.metainfo.xml`) |
| macOS | `Info.plist` and its localization files (`InfoPlist.strings`) |

## License

MetaGlot is released under the MIT License. See `LICENSE` for details.
