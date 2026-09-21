# Render Context

A render context is the set of top-level variables that MetaGlot passes into a user-provided Liquid template when `metaglot render` executes. The context carries the resolved translation data — one entry per language read from the PO files, each holding the text of every manifest entry — together with the extra variables a metadata type needs, such as the manifest's source language or per-language identifiers.

Every rendering shares the following semantics:

- Templates are read as UTF-8, and the rendered output is written as UTF-8 (without BOM) using the system's native line endings. The parent folder of an output file is created when it does not exist.
- The renderer runs in strict mode: referencing a variable or a property that does not exist fails the render.
- The text of an entry falls back to the manifest source string when the entry is untranslated, missing from the PO file, or marked fuzzy.
- The language of a PO file is resolved from its `Language:` header, falling back to the file name without extension; two PO files describing the same language and PO entries unknown to the manifest are rejected.
- Some metadata types consist of multiple files; for them the `--*-path` command line arguments are themselves in-memory Liquid templates, rendered with the same mechanism into per-file output paths.

Filters are documented separately in [filters.md](filters.md).

The render context of every supported metadata type is described in its own document:

- [Windows RC resource files](render-context/rc.md) — language identifiers, string table statements and version information values.
- [Windows MSIX packages](render-context/msix.md) — the package manifest and the per-language resources files.
- [Windows InnoSetup scripts](render-context/inno.md) — the installation script and the per-language messages files.
- [Linux desktop entries](render-context/desktop.md) — localized keys with locale postfixes.
- [Linux AppStream metadata](render-context/appstream.md) — translations marked with `xml:lang`.
- [macOS bundles](render-context/plist.md) — the bundle `Info.plist` and the per-language `InfoPlist.strings` files.
