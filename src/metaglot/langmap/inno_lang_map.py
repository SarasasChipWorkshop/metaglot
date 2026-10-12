import enum
from dataclasses import dataclass

from ..langid import InnoLang, PoLang


class InnoVersion(enum.IntFlag):
    """
    Represents the major versions of Inno Setup, as a flag set.

    A flag combination marks the set of Inno Setup versions a conventional
    language name is official in; ``Nothing`` marks a name that no
    transcribed Inno Setup version bundles.
    """

    Nothing = 0
    Inno6 = enum.auto()
    Inno7 = enum.auto()


@dataclass(frozen=True)
class _InnoLangProp:
    """The properties of one conventional Inno Setup language name."""

    official_vers: InnoVersion
    """The Inno Setup versions the name is official in."""
    ids: tuple[str, ...]
    """Every PO language key converting to the name."""


# YYC MARK:
# Inno Setup language files have no standardized names: both the internal
# names of the [Languages] section and the messages file names are chosen
# freely by the packager. The table below transcribes the *conventional*
# base names of the messages files distributed by the Inno Setup project
# itself, so a PO language can be paired with them without template-side
# case blocks.
#
# The names and the community list come from
# https://jrsoftware.org/files/istrans/ (fetched 2026-10-08). The
# officiality of each name is transcribed from the 'Languages' folder
# listings of the Inno Setup compilers themselves: 6.7.1 backs
# InnoVersion.Inno6 and 7.1.0 backs InnoVersion.Inno7 (both listings
# received 2026-10-12). The two listings differ in four names:
# ChineseSimplified, ChineseTraditional, Lithuanian and Thai are bundled
# since Inno Setup 7 only.
#
# The table is authored name-oriented (_LANGS below, one row per
# conventional name holding its officiality and every PO language key
# converting to it) and the structures used at runtime (the key-oriented
# lookup _INNO_NAMES and the per-version official sets) are derived from
# it, so a name shared by several keys - like ChineseSimplified ('zh',
# 'zh-SG') - is declared exactly once. The keys are hyphenated PO
# language components ('ll', 'll-CC', or variant-aware forms). Keys
# needing country disambiguation are spelled out; every other language is
# reachable through the bare 'll' fallback. Outdated unofficial
# translations are still transcribed - an outdated base file is better
# than an English-only installer - with their minimum supported Inno
# Setup version noted in a trailing comment.
#
# Transcription notes:
# - English has no dedicated file: 'Default.isl' lives at the compiler
#   root, not in the 'Languages' subfolder, so 'en' maps to 'Default'.
#   The folder listings do not cover it; it is treated as official in
#   every version.
# - Known contradiction: the istrans page lists Icelandic as an official
#   translation, but neither the 6.7.1 nor the 7.1.0 'Languages' folder
#   ships it. The folder listings win here, so Icelandic is official in
#   no version.
# - The conventional name is the file BASE name, not the 'LanguageName'
#   field inside the file ('ChineseSimplified' vs 'Chinese (Simplified)').
# - Seven legacy community files ship with a '.islu' extension (Bengali,
#   Hindi, Kazakh, Marathi, Nepali, Sinhala, Uyghur); the table records
#   base names only, and the extension is the template author's concern.

# fmt: off
_LANGS: dict[InnoLang, _InnoLangProp] = {
    # Official in every transcribed version (the 6.7.1 and 7.1.0
    # 'Languages' folder intersection, plus Default).
    InnoLang("Default"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("en",)),  # compiler:Default.isl, at the compiler root.
    InnoLang("Arabic"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("ar",)),
    InnoLang("Armenian"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("hy",)),
    InnoLang("BrazilianPortuguese"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("pt-BR",)),
    InnoLang("Bulgarian"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("bg",)),
    InnoLang("Catalan"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("ca",)),
    InnoLang("Corsican"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("co",)),
    InnoLang("Czech"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("cs",)),
    InnoLang("Danish"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("da",)),
    InnoLang("Dutch"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("nl",)),
    InnoLang("Finnish"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("fi",)),
    InnoLang("French"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("fr",)),
    InnoLang("German"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("de",)),
    InnoLang("Hebrew"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("he",)),
    InnoLang("Hungarian"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("hu",)),
    InnoLang("Italian"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("it",)),
    InnoLang("Japanese"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("ja",)),
    InnoLang("Korean"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("ko",)),
    InnoLang("Norwegian"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("no", "nb")),
    InnoLang("Polish"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("pl",)),
    InnoLang("Portuguese"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("pt",)),
    InnoLang("Russian"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("ru",)),
    InnoLang("Slovak"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("sk",)),
    InnoLang("Slovenian"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("sl",)),
    InnoLang("Spanish"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("es",)),
    InnoLang("Swedish"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("sv",)),
    InnoLang("Tamil"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("ta",)),
    InnoLang("Turkish"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("tr",)),
    InnoLang("Ukrainian"): _InnoLangProp(InnoVersion.Inno6 | InnoVersion.Inno7, ("uk",)),
    # Official since Inno Setup 7 only.
    InnoLang("ChineseSimplified"): _InnoLangProp(InnoVersion.Inno7, ("zh", "zh-SG")),
    InnoLang("ChineseTraditional"): _InnoLangProp(InnoVersion.Inno7, ("zh-TW", "zh-HK", "zh-MO")),
    InnoLang("Lithuanian"): _InnoLangProp(InnoVersion.Inno7, ("lt",)),
    InnoLang("Thai"): _InnoLangProp(InnoVersion.Inno7, ("th",)),
    # Official in no transcribed version (community provided).
    InnoLang("Icelandic"): _InnoLangProp(InnoVersion.Nothing, ("is",)),  # istrans lists it official; no transcribed bundle ships it.
    # Community maintained, up to date with the current Inno Setup.
    InnoLang("Afrikaans"): _InnoLangProp(InnoVersion.Nothing, ("af",)),
    InnoLang("Basque"): _InnoLangProp(InnoVersion.Nothing, ("eu",)),
    InnoLang("Croatian"): _InnoLangProp(InnoVersion.Nothing, ("hr",)),
    InnoLang("EnglishBritish"): _InnoLangProp(InnoVersion.Nothing, ("en-GB",)),
    InnoLang("Galician"): _InnoLangProp(InnoVersion.Nothing, ("gl",)),
    InnoLang("Greek"): _InnoLangProp(InnoVersion.Nothing, ("el",)),
    InnoLang("Esperanto"): _InnoLangProp(InnoVersion.Nothing, ("eo",)),
    InnoLang("Indonesian"): _InnoLangProp(InnoVersion.Nothing, ("id",)),
    InnoLang("Farsi"): _InnoLangProp(InnoVersion.Nothing, ("fa",)),
    InnoLang("Vietnamese"): _InnoLangProp(InnoVersion.Nothing, ("vi",)),
    InnoLang("SerbianCyrillic"): _InnoLangProp(InnoVersion.Nothing, ("sr",)),  # Cyrillic is the default script.
    InnoLang("SerbianLatin"): _InnoLangProp(InnoVersion.Nothing, ("sr-Latn",)),  # e.g. sr_RS@latin.
    # Community maintained, outdated for the current Inno Setup. Minimum versions noted.
    InnoLang("Abkhazian"): _InnoLangProp(InnoVersion.Nothing, ("ab",)),  # outdated: 6.4.0+
    InnoLang("Albanian"): _InnoLangProp(InnoVersion.Nothing, ("sq",)),  # outdated: 6.4.0+
    InnoLang("Azerbaijan"): _InnoLangProp(InnoVersion.Nothing, ("az",)),  # outdated: 6.4.0+
    InnoLang("Bosnian"): _InnoLangProp(InnoVersion.Nothing, ("bs",)),  # outdated: 6.4.0+
    InnoLang("Ewe"): _InnoLangProp(InnoVersion.Nothing, ("ee",)),  # outdated: 6.4.0+
    InnoLang("Belarusian"): _InnoLangProp(InnoVersion.Nothing, ("be",)),  # outdated: 6.1.0+
    InnoLang("Georgian"): _InnoLangProp(InnoVersion.Nothing, ("ka",)),  # outdated: 6.1.0+
    InnoLang("Latvian"): _InnoLangProp(InnoVersion.Nothing, ("lv",)),  # outdated: 6.1.0+
    InnoLang("Montenegrin"): _InnoLangProp(InnoVersion.Nothing, ("cnr",)),  # outdated: 6.1.0+
    InnoLang("Romanian"): _InnoLangProp(InnoVersion.Nothing, ("ro",)),  # outdated: 6.1.0+
    InnoLang("Urdu"): _InnoLangProp(InnoVersion.Nothing, ("ur",)),  # outdated: 6.1.0+
    InnoLang("Uyghur"): _InnoLangProp(InnoVersion.Nothing, ("ug",)),  # outdated: 6.1.0+, ships as .islu
    InnoLang("ScottishGaelic"): _InnoLangProp(InnoVersion.Nothing, ("gd",)),  # outdated: 6.0.0+
    InnoLang("Bengali"): _InnoLangProp(InnoVersion.Nothing, ("bn",)),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Estonian"): _InnoLangProp(InnoVersion.Nothing, ("et",)),  # outdated: 5.5.3+
    InnoLang("Hindi"): _InnoLangProp(InnoVersion.Nothing, ("hi",)),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Marathi"): _InnoLangProp(InnoVersion.Nothing, ("mr",)),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Nepali"): _InnoLangProp(InnoVersion.Nothing, ("ne",)),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Sinhala"): _InnoLangProp(InnoVersion.Nothing, ("si",)),  # outdated: 5.5.3+, ships as .islu
    InnoLang("Uzbek"): _InnoLangProp(InnoVersion.Nothing, ("uz",)),  # outdated: 5.5.3+
    InnoLang("Valencian"): _InnoLangProp(InnoVersion.Nothing, ("ca-ES-valencia",)),  # outdated: 5.5.3+
    InnoLang("Kazakh"): _InnoLangProp(InnoVersion.Nothing, ("kk",)),  # outdated: 5.5.0+, ships as .islu
    InnoLang("Kurdish"): _InnoLangProp(InnoVersion.Nothing, ("ku",)),  # outdated: 5.5.0+
    InnoLang("Tatar"): _InnoLangProp(InnoVersion.Nothing, ("tt",)),  # outdated: 5.5.0+
    InnoLang("Ligurian"): _InnoLangProp(InnoVersion.Nothing, ("lij",)),  # outdated: 5.1.11+
    InnoLang("Luxemburgish"): _InnoLangProp(InnoVersion.Nothing, ("lb",)),  # outdated: 5.1.11+
    InnoLang("Macedonian"): _InnoLangProp(InnoVersion.Nothing, ("mk",)),  # outdated: 5.1.11+
    InnoLang("Mongolian"): _InnoLangProp(InnoVersion.Nothing, ("mn",)),  # outdated: 5.1.11+
    InnoLang("Occitan"): _InnoLangProp(InnoVersion.Nothing, ("oc",)),  # outdated: 5.1.11+
    InnoLang("Malaysian"): _InnoLangProp(InnoVersion.Nothing, ("ms",)),  # outdated: 5.1.0+
    InnoLang("Asturian"): _InnoLangProp(InnoVersion.Nothing, ("ast",)),  # outdated: 4.0.5+
    InnoLang("NorwegianNynorsk"): _InnoLangProp(InnoVersion.Nothing, ("nn",)),  # outdated: 4.0.5+
}
# fmt: on

# The key-oriented lookup table used at runtime. The duplicate check makes
# a transcription mistake - the same PO language key attached to two names
# - fail at import time instead of silently overriding in the
# comprehension below.
_INNO_NAMES: dict[str, InnoLang] = {
    key: name for name, prop in _LANGS.items() for key in prop.ids
}
if len(_INNO_NAMES) != sum(len(prop.ids) for prop in _LANGS.values()):
    raise ValueError("duplicate PO language key(s) in the Inno Setup language table")

# The conventional names bundled with each transcribed Inno Setup version,
# derived from the officiality flags.
_OFFICIAL_NAMES_V6: frozenset[InnoLang] = frozenset(
    name for name, prop in _LANGS.items() if prop.official_vers & InnoVersion.Inno6
)
_OFFICIAL_NAMES_V7: frozenset[InnoLang] = frozenset(
    name for name, prop in _LANGS.items() if prop.official_vers & InnoVersion.Inno7
)
_OFFICIAL_NAMES: dict[InnoVersion, frozenset[InnoLang]] = {
    InnoVersion.Inno6: _OFFICIAL_NAMES_V6,
    InnoVersion.Inno7: _OFFICIAL_NAMES_V7,
}


@dataclass(frozen=True)
class InnoConversion:
    """The result of a best-effort PO language conversion for Inno Setup."""

    name: InnoLang | None
    """The conventional Inno Setup language name, or ``None`` if no
    conventional name exists for the language."""

    official: bool
    """Whether the name belongs to an official translation bundled with
    the targeted Inno Setup version. Always ``False`` when ``name`` is
    ``None``."""


# Gettext-style script designator words mapped to ISO 15924 script codes.
# This is not the full ISO 15924 table - it only contains the words that can
# hit entries in _INNO_NAMES above. Extend it as needed.
_SCRIPT_WORDS: dict[str, str] = {
    "latin": "Latn",
    "cyrillic": "Cyrl",
    "arabic": "Arab",
}


def convert(lang: PoLang, inno_version: InnoVersion) -> InnoConversion:
    """
    Convert a PO file language to a conventional Inno Setup language name.

    The conversion is a best effort: the language, country and variant
    components are hyphenated into candidate keys, variant-aware forms
    first (the PO variant slot may hold a script designator, interpreted
    via the script word table), then the country form, then the bare
    language form. The first candidate hitting the transcription table
    wins. Unlike the other targets, a missing name never raises - a
    language without a conventional name converts to an empty result
    (``name`` is ``None``, ``official`` is ``False``), and the caller
    falls back to the PO language tag. The officiality is judged against
    the given Inno Setup version.

    :param lang: The PO file language.
    :param inno_version: The Inno Setup major version the rendering
        targets. It must be a single-version member, not a combination
        flag.
    :return: The conversion result holding the conventional Inno Setup
        language name (``None`` if none exists) and whether it belongs to
        an official translation bundled with the targeted version.
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
            return InnoConversion(name, name in _OFFICIAL_NAMES[inno_version])
    return InnoConversion(None, False)
