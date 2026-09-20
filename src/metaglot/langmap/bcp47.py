from ..langid import Bcp47Lang, PoLang

# YYC MARK:
# Gettext's variant slot may hold either a script designator or a
# genuine variant, and BCP 47 places the two at different positions with
# different vocabularies ('latin' != 'Latn'), so the conversion cannot be
# done mechanically. Candidate matching is done here as a workaround, with
# the script interpretation tried first: 'sr_RS@latin' becomes the
# semantically correct 'sr-Latn-RS', not 'sr-RS-latin'. This is not the
# full ISO 15924 table, only the words Gettext uses for scripts; extend it
# as needed.
_SCRIPT_WORDS: dict[str, str] = {
    "latin": "Latn",
    "cyrillic": "Cyrl",
    "arabic": "Arab",
}


def convert[T: Bcp47Lang](lang: PoLang, cls: type[T]) -> T:
    """
    Convert a PO file language to a BCP 47 language tag.

    The tag is composed from the rules shared by every BCP 47 based
    target: the language and country codes carry over unchanged
    (hyphenated), and the PO variant slot fills either the script subtag
    or the variant subtag, whichever interpretation the variant word
    supports. The composed tag is validated once by ``cls`` itself during
    the construction: legacy Gettext variants that the IANA registry does
    not register (e.g. 'euro') are rejected there.

    :param lang: The PO file language.
    :param cls: The BCP 47 class to construct, e.g. ``AppStreamLang`` or
        ``MsixLang``.
    :return: The BCP 47 language tag of class ``cls``.
    :raises ValueError: If the composed tag is not a valid BCP 47 tag.
    """
    segments = [lang.language]
    script = _SCRIPT_WORDS.get(lang.variant) if lang.variant is not None else None
    if script is not None:
        segments.append(script)
        if lang.country is not None:
            segments.append(lang.country)
    else:
        if lang.country is not None:
            segments.append(lang.country)
        if lang.variant is not None:
            segments.append(lang.variant)
    return cls("-".join(segments))
