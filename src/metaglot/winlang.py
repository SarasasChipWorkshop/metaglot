from dataclasses import dataclass


@dataclass(frozen=True)
class WindowsLanguage:
    langid: int
    name: str

    @property
    def primary(self) -> int:
        return self.langid & 0x3FF

    @property
    def sublanguage(self) -> int:
        return self.langid >> 10


_LANGUAGES: dict[str, WindowsLanguage] = {
    "en": WindowsLanguage(0x0409, "English (United States)"),
    "ca": WindowsLanguage(0x0403, "Catalan (Catalan)"),
    "de": WindowsLanguage(0x0407, "German (Germany)"),
    "es": WindowsLanguage(0x0C0A, "Spanish (Spain)"),
    "fr": WindowsLanguage(0x040C, "French (France)"),
    "id": WindowsLanguage(0x0421, "Indonesian (Indonesia)"),
    "it": WindowsLanguage(0x0410, "Italian (Italy)"),
    "ja": WindowsLanguage(0x0411, "Japanese (Japan)"),
    "ko": WindowsLanguage(0x0412, "Korean (Korea)"),
    "nb_NO": WindowsLanguage(0x0414, "Norwegian Bokmal (Norway)"),
    "nl": WindowsLanguage(0x0413, "Dutch (Netherlands)"),
    "pa_PK": WindowsLanguage(0x0846, "Punjabi (Pakistan)"),
    "ru": WindowsLanguage(0x0419, "Russian (Russia)"),
    "si": WindowsLanguage(0x045B, "Sinhala (Sri Lanka)"),
    "sl": WindowsLanguage(0x0424, "Slovenian (Slovenia)"),
    "ta": WindowsLanguage(0x0449, "Tamil (India)"),
    "tr": WindowsLanguage(0x041F, "Turkish (Turkey)"),
    "uk": WindowsLanguage(0x0422, "Ukrainian (Ukraine)"),
    "vi": WindowsLanguage(0x042A, "Vietnamese (Vietnam)"),
    "zh_CN": WindowsLanguage(0x0804, "Chinese (Simplified, China)"),
}

_ALIASES: dict[str, str] = {
    "en_US": "en",
    "en_GB": "en",
    "zh": "zh_CN",
    "zh_Hans": "zh_CN",
    "zh_Hans_CN": "zh_CN",
    "nb": "nb_NO",
    "no": "nb_NO",
    "pa": "pa_PK",
}


def lookup(locale: str) -> WindowsLanguage:
    normalized = locale.replace("-", "_")
    if normalized in _LANGUAGES:
        return _LANGUAGES[normalized]
    if normalized in _ALIASES:
        return _LANGUAGES[_ALIASES[normalized]]
    raise KeyError(locale)
