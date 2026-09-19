# Developer Notes

This document introduces some notes for the developer of MetaGlot.

## Reference

This chapter introduces all references used when developing MetaGlot.

### PO File

We fetch the standard of `Language` field of metadata of PO file from [GNU Gettext document](https://www.gnu.org/software/gettext/manual/html_node/Header-Entry.html). And we use it to create the representation of PO file language.

### Windows RC File

Some constant values located in Windows RC file rely on Microsoft LCID. We use [Microsoft provided LCID document](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/70feba9f-294e-491e-b6eb-56532684c37f) to create LCID representation and convertion code which converts PO file language representation to LCID representation. The adopted version of this specification is **revision 2024-04-23**.

The string used in Windows RC file is basically C string literal. We design corresponding Liquid filter based on this.

### `.desktop` File

We browse [FreeDesktop provided `.desktop` file format document](https://specifications.freedesktop.org/desktop-entry/1.5/localized-keys.html) to get the standard of its localized key. Then we use it to create the representation of `.desktop` file language, and convertion code which converts PO file language representation to this representation. The adopted version of specification is **1.5**.

We also browse [FreeDesktop provided document about valid string format in `.desktop` file](https://specifications.freedesktop.org/desktop-entry/1.5/value-types.html), and create corresponding Liquid filter based on it.

### AppStream Metadata File

AppStream XML file use standard `xml:lang` attribute to mark its languages and locales. According to the [standard of XML](https://www.w3.org/TR/REC-xml/), the value of it must follow BCP 47. We use it to design the representation of AppStream metadata file language, and convertion code which converts PO file language representation to this representation.

Based on the example AppStream metadata file, all strings which need to be inserted are located between two XML labels, or at the value of attribute. So we simply create corresponding Liquid filter according to the [standard of XML](https://www.w3.org/TR/REC-xml/).

### Windows MSIX Files

Windows MSIX involves multiple file formats. All formats of them can be browsed from their official documents:

- `Package.appxmanifest` (for Visual Studio project use) and `AppxManifest.xml` (for final delivery): https://learn.microsoft.com/en-us/uwp/schemas/appxpackage/uapmanifestschema/schema-root
- `.resw` and `.resjson` file: https://learn.microsoft.com/en-us/previous-versions/windows/apps/jj552944

We use these formats to create Liquid filters.

Additionally, we check [the document about localization file path](https://learn.microsoft.com/en-us/windows/uwp/app-resources/localize-strings-ui-manifest) to know the language tag used by Windows MSIX. Then we use it to create the representation of it, and convertion code which converts PO file language representation to this representation.

## Bump Version Up

### Bump Application Version Up

TODO...

### Bump Manifest Version Up

- Update version value in document `doc/manifest.md`.
- Update version value in example `doc/example.*.toml`.
