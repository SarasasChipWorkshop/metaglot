from dataclasses import dataclass

from ..langid import InnoLang, PoLang

# YYC MARK:
# Inno Setup language files have no standardized names: both the internal
# names of the [Languages] section and the messages file names are chosen
# freely by the packager. The tables below transcribe the *conventional*
# base names of the messages files distributed by the Inno Setup project
# itself, so a PO language can be paired with them without template-side
# case blocks.
#
# The official translations are bundled with Inno Setup (in the compiler's
# 'Languages' subfolder), and the unofficial ones are community maintained.
# Both lists were fetched from https://jrsoftware.org/files/istrans/ on
# 2026-10-08, reflecting Inno Setup 6.5.0+. The official/unofficial split
# is kept as two separate seed tables, so it stays machine-readable: the
# officiality of a conversion is exposed to templates as 'is_official',
# letting them serve users with a bare Inno Setup installation.
#
# The tables are authored name-oriented (_OFFICIAL_NAME_KEYS and
# _UNOFFICIAL_NAME_KEYS below, one row per conventional name holding every
# PO language key converting to it) and the key-oriented lookup used at
# runtime (_INNO_NAMES) is derived from them, so a name shared by several
# keys - like ChineseSimplified ('zh', 'zh-SG') - is declared exactly once.
# The keys are hyphenated PO language components ('ll', 'll-CC', or
# variant-aware forms). Keys needing country disambiguation are spelled
# out; every other language is reachable through the bare 'll' fallback.
# Outdated unofficial translations are still transcribed - an outdated
# base file is better than an English-only installer - with their minimum
# supported Inno Setup version noted in a trailing comment.
#
# Transcription notes:
# - English has no dedicated file: 'Default.isl' lives at the compiler
#   root, not in the 'Languages' subfolder, so 'en' maps to 'Default'.
# - The conventional name is the file BASE name, not the 'LanguageName'
#   field inside the file ('ChineseSimplified' vs 'Chinese (Simplified)').
# - Seven legacy unofficial files ship with a '.islu' extension (Bengali,
#   Hindi, Kazakh, Marathi, Nepali, Sinhala, Uyghur); the tables record
#   base names only, and the extension is the template author's concern.

# fmt: off
_OFFICIAL_NAME_KEYS: dict[InnoLang, tuple[str, ...]] = {
    # Official translations (bundled with Inno Setup).
    InnoLang("Default"): ("en",),  # compiler:Default.isl, at the compiler root.
    InnoLang("Arabic"): ("ar",),
    InnoLang("Armenian"): ("hy",),
    InnoLang("Bulgarian"): ("bg",),
    InnoLang("Catalan"): ("ca",),
    InnoLang("ChineseSimplified"): ("zh", "zh-SG"),
    InnoLang("ChineseTraditional"): ("zh-TW", "zh-HK", "zh-MO"),
    InnoLang("Corsican"): ("co",),
    InnoLang("Czech"): ("cs",),
    InnoLang("Danish"): ("da",),
    InnoLang("Dutch"): ("nl",),
    InnoLang("Finnish"): ("fi",),
    InnoLang("French"): ("fr",),
    InnoLang("German"): ("de",),
    InnoLang("Hebrew"): ("he",),
    InnoLang("Hungarian"): ("hu",),
    InnoLang("Icelandic"): ("is",),
    InnoLang("Italian"): ("it",),
    InnoLang("Japanese"): ("ja",),
    InnoLang("Korean"): ("ko",),
    InnoLang("Lithuanian"): ("lt",),
    InnoLang("Norwegian"): ("no", "nb"),
    InnoLang("Polish"): ("pl",),
    InnoLang("Portuguese"): ("pt",),
    InnoLang("BrazilianPortuguese"): ("pt-BR",),
    InnoLang("Russian"): ("ru",),
    InnoLang("Slovak"): ("sk",),
    InnoLang("Slovenian"): ("sl",),
    InnoLang("Spanish"): ("es",),
    InnoLang("Swedish"): ("sv",),
    InnoLang("Tamil"): ("ta",),
    InnoLang("Thai"): ("th",),
    InnoLang("Turkish"): ("tr",),
    InnoLang("Ukrainian"): ("uk",),
}

_UNOFFICIAL_NAME_KEYS: dict[InnoLang, tuple[str, ...]] = {
    # Community maintained translations, up to date with 6.5.0+.
    InnoLang("Afrikaans"): ("af",),
    InnoLang("Basque"): ("eu",),
    InnoLang("Croatian"): ("hr",),
    InnoLang("EnglishBritish"): ("en-GB",),
    InnoLang("Galician"): ("gl",),
    InnoLang("Greek"): ("el",),
    InnoLang("Esperanto"): ("eo",),
    InnoLang("Indonesian"): ("id",),
    InnoLang("Farsi"): ("fa",),
    InnoLang("Vietnamese"): ("vi",),
    InnoLang("SerbianCyrillic"): ("sr",),  # Cyrillic is the default script.
    InnoLang("SerbianLatin"): ("sr-Latn",),  # e.g. sr_RS@latin.
    # Community maintained translations, outdated for 6.5.0. Minimum versions noted.
    InnoLang("Abkhazian"): ("ab",),  # outdated: 6.4.0+
    InnoLang("Albanian"): ("sq",),  # outdated: 6.4.0+
    InnoLang("Azerbaijan"): ("az",),  # outdated: 6.4.0+
    InnoLang("Bosnian"): ("bs",),  # outdated: 6.4.0+
    InnoLang("Ewe"): ("ee",),  # outdated: 6.4.0+
    InnoLang("Belarusian"): ("be",),  # outdated: 6.1.0+
    InnoLang("Georgian"): ("ka",),  # outdated: 6.1.0+
    InnoLang("Latvian"): ("lv",),  # outdated: 6.1.0+
    InnoLang("Montenegrin"): ("cnr",),  # outdated: 6.1.0+
    InnoLang("Romanian"): ("ro",),  # outdated: 6.1.0+
    InnoLang("Urdu"): ("ur",),  # outdated: 6.1.0+
    InnoLang("Uyghur"): ("ug",),  # outdated: 6.1.0+, ships as .islu
    InnoLang("ScottishGaelic"): ("gd",),  # outdated: 6.0.0+
    InnoLang("Bengali"): ("bn",),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Estonian"): ("et",),  # outdated: 5.5.3+
    InnoLang("Hindi"): ("hi",),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Marathi"): ("mr",),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Nepali"): ("ne",),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Sinhala"): ("si",),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Uzbek"): ("uz",),  # outdated: 5.5.3+
    InnoLang("Valencian"): ("ca-ES-valencia",),  # outdated: 5.5.3+
    InnoLang("Kazakh"): ("kk",),  # outdated: 5.5.0+, ships as .islu
    InnoLang("Kurdish"): ("ku",),  # outdated: 5.5.0+
    InnoLang("Tatar"): ("tt",),  # outdated: 5.5.0+
    InnoLang("Ligurian"): ("lij",),  # outdated: 5.1.11+
    InnoLang("Luxemburgish"): ("lb",),  # outdated: 5.1.11+
    InnoLang("Macedonian"): ("mk",),  # outdated: 5.1.11+
    InnoLang("Mongolian"): ("mn",),  # outdated: 5.1.11+
    InnoLang("Occitan"): ("oc",),  # outdated: 5.1.11+
    InnoLang("Malaysian"): ("ms",),  # outdated: 5.1.0+
    InnoLang("Asturian"): ("ast",),  # outdated: 4.0.5+
    InnoLang("NorwegianNynorsk"): ("nn",),  # outdated: 4.0.5+
}
# fmt: on

# The key-oriented lookup table used at runtime, derived from both seed
# tables. The duplicate check makes a transcription mistake - the same PO
# language key attached to two names - fail at import time instead of
# silently overriding in the comprehension below.
_INNO_NAMES: dict[str, InnoLang] = {
    key: name
    for names in (_OFFICIAL_NAME_KEYS, _UNOFFICIAL_NAME_KEYS)
    for name, keys in names.items()
    for key in keys
}
if len(_INNO_NAMES) != sum(
    len(keys) for names in (_OFFICIAL_NAME_KEYS, _UNOFFICIAL_NAME_KEYS) for keys in names.values()
):
    raise ValueError("duplicate PO language key(s) in the Inno Setup name table")

# The conventional names that belong to official translations, i.e. the
# messages files bundled with the Inno Setup compiler itself.
_OFFICIAL_NAMES: frozenset[InnoLang] = frozenset(_OFFICIAL_NAME_KEYS)


@dataclass(frozen=True)
class InnoConversion:
    """The result of a best-effort PO language conversion for Inno Setup."""

    name: InnoLang | None
    """The conventional Inno Setup language name, or ``None`` if no
    conventional name exists for the language."""

    official: bool
    """Whether the name belongs to an official translation bundled with
    Inno Setup. Always ``False`` when ``name`` is ``None``."""


# Gettext-style script designator words mapped to ISO 15924 script codes.
# This is not the full ISO 15924 table - it only contains the words that can
# hit entries in _INNO_NAMES above. Extend it as needed.
_SCRIPT_WORDS: dict[str, str] = {
    "latin": "Latn",
    "cyrillic": "Cyrl",
    "arabic": "Arab",
}


def convert(lang: PoLang) -> InnoConversion:
    """
    Convert a PO file language to a conventional Inno Setup language name.

    The conversion is a best effort: the language, country and variant
    components are hyphenated into candidate keys, variant-aware forms
    first (the PO variant slot may hold a script designator, interpreted
    via the script word table), then the country form, then the bare
    language form. The first candidate hitting the transcription table
    wins. Unlike the other targets, no exception is ever raised - a
    language without a conventional name converts to an empty result
    (``name`` is ``None``, ``official`` is ``False``), and the caller
    falls back to the PO language tag.

    :param lang: The PO file language.
    :return: The conversion result holding the conventional Inno Setup
        language name (``None`` if none exists) and whether it belongs to
        an official translation bundled with Inno Setup.
    """
    candidates: list[str] = []
    if lang.variant is not None:
        script = _SCRIPT_WORDS.get(lang.variant)
        if script is not None:
            # Script interpretation: 'sr_RS@latin' -> 'sr-Latn-RS'.
            candidates.append(f"{lang.language}-{script}-{lang.country}")
            candidates.append(f"{lang.language}-{script}")
        else:
            # Variant interpretation: 'ca_ES@valencia' -> 'ca-ES-valencia'.
            candidates.append(f"{lang.language}-{lang.country}-{lang.variant}")
            candidates.append(f"{lang.language}-{lang.variant}")
    if lang.country is not None:
        candidates.append(f"{lang.language}-{lang.country}")
    candidates.append(lang.language)
    for candidate in candidates:
        name = _INNO_NAMES.get(candidate)
        if name is not None:
            return InnoConversion(name, name in _OFFICIAL_NAMES)
    return InnoConversion(None, False)
