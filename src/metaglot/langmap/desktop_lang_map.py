from ..langid import DesktopLang, PoLang


# YYC MARK:
# The standard of this convertion procedure can be seen at:
# https://specifications.freedesktop.org/desktop-entry/1.5/localized-keys.html
# The adopted version of specification is **1.5** .


def convert(lang: PoLang) -> DesktopLang:
    """
    Convert a PO file language to a desktop entry locale.

    Both sides speak ISO codes and share the same component layout, so the
    conversion maps components one to one: the language and country codes
    carry over unchanged, and the PO variant slot fills the desktop
    modifier slot. No lookup table is needed here - unlike the Windows
    map, whose vocabulary differs on both sides ('cyrillic' != 'Cyrl') -
    which keeps this module the extension point should special cases
    emerge.

    :param lang: The PO file language.
    :return: The desktop entry locale for the language.
    """
    segments = [lang.language]
    if lang.country is not None:
        segments.append(lang.country)
    value = "_".join(segments)
    if lang.variant is not None:
        value += f"@{lang.variant}"
    return DesktopLang(value)
