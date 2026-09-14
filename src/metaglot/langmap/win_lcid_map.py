from ..langid import PoLang, WinLcid

# YYC MARK: The table below is transcribed from the 'Language ID' table in
# [MS-LCID] section 2.2 (revision 2024-04-23). Underscore separators in the
# original language tags have been normalized to hyphens
# (e.g. 'es-ES_tradnl' -> 'es-ES-tradnl').
# YYC MARK: Rows whose tags are marked 'reserved' in the document are kept
# for transcription fidelity but commented out with a leading '#', so they
# carry no runtime effect and lookups on them fail.
# YYC MARK: Rows without a usable language tag are omitted entirely: values
# that are neither defined nor reserved, the invariant-locale value 0x007F,
# the user-default and unspecified placeholders 0x0C00/0x1000 (harmful
# process-local values that must never be persisted into RC resources), and
# the transient LCIDs 0x2000-0x4C00.
# YYC MARK: Rows carrying multiple tags for one value (e.g.
# 'ff-NG, ff-Latn-NG') are expanded into consecutive entries sharing the
# same WinLcid.
# YYC MARK: The alternate-sort table of section 2.2 (full 4-byte LCIDs with
# sort identifiers, e.g. 'de-DE_phoneb' 0x00010407) is not transcribed:
# WinLcid only models the 2-byte language identifier used by RC resources.
# YYC MARK: Known contradiction inside the document: the appendix assigns
# 'quc' -> 0x0086 and 'quc-Latn-GT' -> 0x0486, while the section 2.2 registry
# has 'qut' -> 0x0086 and marks 'quc' (0x0093), 'qut-GT' (0x0486) and
# 'quc-CO' (0x0493) as reserved. The section 2.2 registry wins here.

_LCID_TAGS: dict[str, WinLcid] = {
    "ar": WinLcid(0x0001),
    "bg": WinLcid(0x0002),
    "ca": WinLcid(0x0003),
    "zh-Hans": WinLcid(0x0004),
    "cs": WinLcid(0x0005),
    "da": WinLcid(0x0006),
    "de": WinLcid(0x0007),
    "el": WinLcid(0x0008),
    "en": WinLcid(0x0009),
    "es": WinLcid(0x000A),
    "fi": WinLcid(0x000B),
    "fr": WinLcid(0x000C),
    "he": WinLcid(0x000D),
    "hu": WinLcid(0x000E),
    "is": WinLcid(0x000F),
    "it": WinLcid(0x0010),
    "ja": WinLcid(0x0011),
    "ko": WinLcid(0x0012),
    "nl": WinLcid(0x0013),
    "no": WinLcid(0x0014),
    "pl": WinLcid(0x0015),
    "pt": WinLcid(0x0016),
    "rm": WinLcid(0x0017),
    "ro": WinLcid(0x0018),
    "ru": WinLcid(0x0019),
    "hr": WinLcid(0x001A),
    "sk": WinLcid(0x001B),
    "sq": WinLcid(0x001C),
    "sv": WinLcid(0x001D),
    "th": WinLcid(0x001E),
    "tr": WinLcid(0x001F),
    "ur": WinLcid(0x0020),
    "id": WinLcid(0x0021),
    "uk": WinLcid(0x0022),
    "be": WinLcid(0x0023),
    "sl": WinLcid(0x0024),
    "et": WinLcid(0x0025),
    "lv": WinLcid(0x0026),
    "lt": WinLcid(0x0027),
    "tg": WinLcid(0x0028),
    "fa": WinLcid(0x0029),
    "vi": WinLcid(0x002A),
    "hy": WinLcid(0x002B),
    "az": WinLcid(0x002C),
    "eu": WinLcid(0x002D),
    "hsb": WinLcid(0x002E),
    "mk": WinLcid(0x002F),
    "st": WinLcid(0x0030),
    "ts": WinLcid(0x0031),
    "tn": WinLcid(0x0032),
    "ve": WinLcid(0x0033),
    "xh": WinLcid(0x0034),
    "zu": WinLcid(0x0035),
    "af": WinLcid(0x0036),
    "ka": WinLcid(0x0037),
    "fo": WinLcid(0x0038),
    "hi": WinLcid(0x0039),
    "mt": WinLcid(0x003A),
    "se": WinLcid(0x003B),
    "ga": WinLcid(0x003C),
    # "yi": WinLcid(0x003D),  # reserved
    "ms": WinLcid(0x003E),
    "kk": WinLcid(0x003F),
    "ky": WinLcid(0x0040),
    "sw": WinLcid(0x0041),
    "tk": WinLcid(0x0042),
    "uz": WinLcid(0x0043),
    "tt": WinLcid(0x0044),
    "bn": WinLcid(0x0045),
    "pa": WinLcid(0x0046),
    "gu": WinLcid(0x0047),
    "or": WinLcid(0x0048),
    "ta": WinLcid(0x0049),
    "te": WinLcid(0x004A),
    "kn": WinLcid(0x004B),
    "ml": WinLcid(0x004C),
    "as": WinLcid(0x004D),
    "mr": WinLcid(0x004E),
    "sa": WinLcid(0x004F),
    "mn": WinLcid(0x0050),
    "bo": WinLcid(0x0051),
    "cy": WinLcid(0x0052),
    "km": WinLcid(0x0053),
    "lo": WinLcid(0x0054),
    "my": WinLcid(0x0055),
    "gl": WinLcid(0x0056),
    "kok": WinLcid(0x0057),
    # "mni": WinLcid(0x0058),  # reserved
    "sd": WinLcid(0x0059),
    "syr": WinLcid(0x005A),
    "si": WinLcid(0x005B),
    "chr": WinLcid(0x005C),
    "iu": WinLcid(0x005D),
    "am": WinLcid(0x005E),
    "tzm": WinLcid(0x005F),
    "ks": WinLcid(0x0060),
    "ne": WinLcid(0x0061),
    "fy": WinLcid(0x0062),
    "ps": WinLcid(0x0063),
    "fil": WinLcid(0x0064),
    "dv": WinLcid(0x0065),
    # "bin": WinLcid(0x0066),  # reserved
    "ff": WinLcid(0x0067),
    "ha": WinLcid(0x0068),
    # "ibb": WinLcid(0x0069),  # reserved
    "yo": WinLcid(0x006A),
    "quz": WinLcid(0x006B),
    "nso": WinLcid(0x006C),
    "ba": WinLcid(0x006D),
    "lb": WinLcid(0x006E),
    "kl": WinLcid(0x006F),
    "ig": WinLcid(0x0070),
    # "kr": WinLcid(0x0071),  # reserved
    "om": WinLcid(0x0072),
    "ti": WinLcid(0x0073),
    "gn": WinLcid(0x0074),
    "haw": WinLcid(0x0075),
    # "la": WinLcid(0x0076),  # reserved
    # "so": WinLcid(0x0077),  # reserved
    "ii": WinLcid(0x0078),
    # "pap": WinLcid(0x0079),  # reserved
    "arn": WinLcid(0x007A),
    "moh": WinLcid(0x007C),
    "br": WinLcid(0x007E),
    "ug": WinLcid(0x0080),
    "mi": WinLcid(0x0081),
    "oc": WinLcid(0x0082),
    "co": WinLcid(0x0083),
    "gsw": WinLcid(0x0084),
    "sah": WinLcid(0x0085),
    "qut": WinLcid(0x0086),
    "rw": WinLcid(0x0087),
    "wo": WinLcid(0x0088),
    "prs": WinLcid(0x008C),
    "gd": WinLcid(0x0091),
    "ku": WinLcid(0x0092),
    # "quc": WinLcid(0x0093),  # reserved
    "ar-SA": WinLcid(0x0401),
    "bg-BG": WinLcid(0x0402),
    "ca-ES": WinLcid(0x0403),
    "zh-TW": WinLcid(0x0404),
    "cs-CZ": WinLcid(0x0405),
    "da-DK": WinLcid(0x0406),
    "de-DE": WinLcid(0x0407),
    "el-GR": WinLcid(0x0408),
    "en-US": WinLcid(0x0409),
    "es-ES-tradnl": WinLcid(0x040A),
    "fi-FI": WinLcid(0x040B),
    "fr-FR": WinLcid(0x040C),
    "he-IL": WinLcid(0x040D),
    "hu-HU": WinLcid(0x040E),
    "is-IS": WinLcid(0x040F),
    "it-IT": WinLcid(0x0410),
    "ja-JP": WinLcid(0x0411),
    "ko-KR": WinLcid(0x0412),
    "nl-NL": WinLcid(0x0413),
    "nb-NO": WinLcid(0x0414),
    "pl-PL": WinLcid(0x0415),
    "pt-BR": WinLcid(0x0416),
    "rm-CH": WinLcid(0x0417),
    "ro-RO": WinLcid(0x0418),
    "ru-RU": WinLcid(0x0419),
    "hr-HR": WinLcid(0x041A),
    "sk-SK": WinLcid(0x041B),
    "sq-AL": WinLcid(0x041C),
    "sv-SE": WinLcid(0x041D),
    "th-TH": WinLcid(0x041E),
    "tr-TR": WinLcid(0x041F),
    "ur-PK": WinLcid(0x0420),
    "id-ID": WinLcid(0x0421),
    "uk-UA": WinLcid(0x0422),
    "be-BY": WinLcid(0x0423),
    "sl-SI": WinLcid(0x0424),
    "et-EE": WinLcid(0x0425),
    "lv-LV": WinLcid(0x0426),
    "lt-LT": WinLcid(0x0427),
    "tg-Cyrl-TJ": WinLcid(0x0428),
    "fa-IR": WinLcid(0x0429),
    "vi-VN": WinLcid(0x042A),
    "hy-AM": WinLcid(0x042B),
    "az-Latn-AZ": WinLcid(0x042C),
    "eu-ES": WinLcid(0x042D),
    "hsb-DE": WinLcid(0x042E),
    "mk-MK": WinLcid(0x042F),
    "st-ZA": WinLcid(0x0430),
    "ts-ZA": WinLcid(0x0431),
    "tn-ZA": WinLcid(0x0432),
    "ve-ZA": WinLcid(0x0433),
    "xh-ZA": WinLcid(0x0434),
    "zu-ZA": WinLcid(0x0435),
    "af-ZA": WinLcid(0x0436),
    "ka-GE": WinLcid(0x0437),
    "fo-FO": WinLcid(0x0438),
    "hi-IN": WinLcid(0x0439),
    "mt-MT": WinLcid(0x043A),
    "se-NO": WinLcid(0x043B),
    "yi-001": WinLcid(0x043D),
    "ms-MY": WinLcid(0x043E),
    "kk-KZ": WinLcid(0x043F),
    "ky-KG": WinLcid(0x0440),
    "sw-KE": WinLcid(0x0441),
    "tk-TM": WinLcid(0x0442),
    "uz-Latn-UZ": WinLcid(0x0443),
    "tt-RU": WinLcid(0x0444),
    "bn-IN": WinLcid(0x0445),
    "pa-IN": WinLcid(0x0446),
    "gu-IN": WinLcid(0x0447),
    "or-IN": WinLcid(0x0448),
    "ta-IN": WinLcid(0x0449),
    "te-IN": WinLcid(0x044A),
    "kn-IN": WinLcid(0x044B),
    "ml-IN": WinLcid(0x044C),
    "as-IN": WinLcid(0x044D),
    "mr-IN": WinLcid(0x044E),
    "sa-IN": WinLcid(0x044F),
    "mn-MN": WinLcid(0x0450),
    "bo-CN": WinLcid(0x0451),
    "cy-GB": WinLcid(0x0452),
    "km-KH": WinLcid(0x0453),
    "lo-LA": WinLcid(0x0454),
    "my-MM": WinLcid(0x0455),
    "gl-ES": WinLcid(0x0456),
    "kok-IN": WinLcid(0x0457),
    # "mni-IN": WinLcid(0x0458),  # reserved
    # "sd-Deva-IN": WinLcid(0x0459),  # reserved
    "syr-SY": WinLcid(0x045A),
    "si-LK": WinLcid(0x045B),
    "chr-Cher-US": WinLcid(0x045C),
    "iu-Cans-CA": WinLcid(0x045D),
    "am-ET": WinLcid(0x045E),
    "tzm-Arab-MA": WinLcid(0x045F),
    "ks-Arab": WinLcid(0x0460),
    "ne-NP": WinLcid(0x0461),
    "fy-NL": WinLcid(0x0462),
    "ps-AF": WinLcid(0x0463),
    "fil-PH": WinLcid(0x0464),
    "dv-MV": WinLcid(0x0465),
    # "bin-NG": WinLcid(0x0466),  # reserved
    "ff-NG": WinLcid(0x0467),
    "ff-Latn-NG": WinLcid(0x0467),
    "ha-Latn-NG": WinLcid(0x0468),
    # "ibb-NG": WinLcid(0x0469),  # reserved
    "yo-NG": WinLcid(0x046A),
    "quz-BO": WinLcid(0x046B),
    "nso-ZA": WinLcid(0x046C),
    "ba-RU": WinLcid(0x046D),
    "lb-LU": WinLcid(0x046E),
    "kl-GL": WinLcid(0x046F),
    "ig-NG": WinLcid(0x0470),
    "kr-Latn-NG": WinLcid(0x0471),
    "om-ET": WinLcid(0x0472),
    "ti-ET": WinLcid(0x0473),
    "gn-PY": WinLcid(0x0474),
    "haw-US": WinLcid(0x0475),
    "la-VA": WinLcid(0x0476),
    "so-SO": WinLcid(0x0477),
    "ii-CN": WinLcid(0x0478),
    # "pap-029": WinLcid(0x0479),  # reserved
    "arn-CL": WinLcid(0x047A),
    "moh-CA": WinLcid(0x047C),
    "br-FR": WinLcid(0x047E),
    "ug-CN": WinLcid(0x0480),
    "mi-NZ": WinLcid(0x0481),
    "oc-FR": WinLcid(0x0482),
    "co-FR": WinLcid(0x0483),
    "gsw-FR": WinLcid(0x0484),
    "sah-RU": WinLcid(0x0485),
    # "qut-GT": WinLcid(0x0486),  # reserved
    "rw-RW": WinLcid(0x0487),
    "wo-SN": WinLcid(0x0488),
    "prs-AF": WinLcid(0x048C),
    # "plt-MG": WinLcid(0x048D),  # reserved
    # "zh-yue-HK": WinLcid(0x048E),  # reserved
    # "tdd-Tale-CN": WinLcid(0x048F),  # reserved
    # "khb-Talu-CN": WinLcid(0x0490),  # reserved
    "gd-GB": WinLcid(0x0491),
    "ku-Arab-IQ": WinLcid(0x0492),
    # "quc-CO": WinLcid(0x0493),  # reserved
    "qps-ploc": WinLcid(0x0501),
    "qps-ploca": WinLcid(0x05FE),
    "ar-IQ": WinLcid(0x0801),
    "ca-ES-valencia": WinLcid(0x0803),
    "zh-CN": WinLcid(0x0804),
    "de-CH": WinLcid(0x0807),
    "en-GB": WinLcid(0x0809),
    "es-MX": WinLcid(0x080A),
    "fr-BE": WinLcid(0x080C),
    "it-CH": WinLcid(0x0810),
    # "ja-Ploc-JP": WinLcid(0x0811),  # reserved
    "nl-BE": WinLcid(0x0813),
    "nn-NO": WinLcid(0x0814),
    "pt-PT": WinLcid(0x0816),
    "ro-MD": WinLcid(0x0818),
    "ru-MD": WinLcid(0x0819),
    "sr-Latn-CS": WinLcid(0x081A),
    "sv-FI": WinLcid(0x081D),
    "ur-IN": WinLcid(0x0820),
    # "az-Cyrl-AZ": WinLcid(0x082C),  # reserved
    "dsb-DE": WinLcid(0x082E),
    "tn-BW": WinLcid(0x0832),
    "se-SE": WinLcid(0x083B),
    "ga-IE": WinLcid(0x083C),
    "ms-BN": WinLcid(0x083E),
    # "kk-Latn-KZ": WinLcid(0x083F),  # reserved
    # "uz-Cyrl-UZ": WinLcid(0x0843),  # reserved
    "bn-BD": WinLcid(0x0845),
    "pa-Arab-PK": WinLcid(0x0846),
    "ta-LK": WinLcid(0x0849),
    # "mn-Mong-CN": WinLcid(0x0850),  # reserved
    # "bo-BT": WinLcid(0x0851),  # reserved
    "sd-Arab-PK": WinLcid(0x0859),
    "iu-Latn-CA": WinLcid(0x085D),
    "tzm-Latn-DZ": WinLcid(0x085F),
    "ks-Deva-IN": WinLcid(0x0860),
    "ne-IN": WinLcid(0x0861),
    "ff-Latn-SN": WinLcid(0x0867),
    "quz-EC": WinLcid(0x086B),
    "ti-ER": WinLcid(0x0873),
    "qps-plocm": WinLcid(0x09FF),
    "ar-EG": WinLcid(0x0C01),
    "zh-HK": WinLcid(0x0C04),
    "de-AT": WinLcid(0x0C07),
    "en-AU": WinLcid(0x0C09),
    "es-ES": WinLcid(0x0C0A),
    "fr-CA": WinLcid(0x0C0C),
    "sr-Cyrl-CS": WinLcid(0x0C1A),
    "se-FI": WinLcid(0x0C3B),
    "mn-Mong-MN": WinLcid(0x0C50),
    "dz-BT": WinLcid(0x0C51),
    # "tmz-MA": WinLcid(0x0C5F),  # reserved
    "quz-PE": WinLcid(0x0C6B),
    "ar-LY": WinLcid(0x1001),
    "zh-SG": WinLcid(0x1004),
    "de-LU": WinLcid(0x1007),
    "en-CA": WinLcid(0x1009),
    "es-GT": WinLcid(0x100A),
    "fr-CH": WinLcid(0x100C),
    "hr-BA": WinLcid(0x101A),
    "smj-NO": WinLcid(0x103B),
    "tzm-Tfng-MA": WinLcid(0x105F),
    "ar-DZ": WinLcid(0x1401),
    "zh-MO": WinLcid(0x1404),
    "de-LI": WinLcid(0x1407),
    "en-NZ": WinLcid(0x1409),
    "es-CR": WinLcid(0x140A),
    "fr-LU": WinLcid(0x140C),
    "bs-Latn-BA": WinLcid(0x141A),
    "smj-SE": WinLcid(0x143B),
    "ar-MA": WinLcid(0x1801),
    "en-IE": WinLcid(0x1809),
    "es-PA": WinLcid(0x180A),
    "fr-MC": WinLcid(0x180C),
    "sr-Latn-BA": WinLcid(0x181A),
    "sma-NO": WinLcid(0x183B),
    "ar-TN": WinLcid(0x1C01),
    "en-ZA": WinLcid(0x1C09),
    "es-DO": WinLcid(0x1C0A),
    "fr-029": WinLcid(0x1C0C),
    "sr-Cyrl-BA": WinLcid(0x1C1A),
    "sma-SE": WinLcid(0x1C3B),
    "ar-OM": WinLcid(0x2001),
    "en-JM": WinLcid(0x2009),
    "es-VE": WinLcid(0x200A),
    "fr-RE": WinLcid(0x200C),
    "bs-Cyrl-BA": WinLcid(0x201A),
    "sms-FI": WinLcid(0x203B),
    "ar-YE": WinLcid(0x2401),
    # "en-029": WinLcid(0x2409),  # reserved
    "es-CO": WinLcid(0x240A),
    "fr-CD": WinLcid(0x240C),
    "sr-Latn-RS": WinLcid(0x241A),
    "smn-FI": WinLcid(0x243B),
    "ar-SY": WinLcid(0x2801),
    "en-BZ": WinLcid(0x2809),
    "es-PE": WinLcid(0x280A),
    "fr-SN": WinLcid(0x280C),
    "sr-Cyrl-RS": WinLcid(0x281A),
    "ar-JO": WinLcid(0x2C01),
    "en-TT": WinLcid(0x2C09),
    "es-AR": WinLcid(0x2C0A),
    "fr-CM": WinLcid(0x2C0C),
    "sr-Latn-ME": WinLcid(0x2C1A),
    "ar-LB": WinLcid(0x3001),
    "en-ZW": WinLcid(0x3009),
    "es-EC": WinLcid(0x300A),
    "fr-CI": WinLcid(0x300C),
    "sr-Cyrl-ME": WinLcid(0x301A),
    "ar-KW": WinLcid(0x3401),
    "en-PH": WinLcid(0x3409),
    "es-CL": WinLcid(0x340A),
    "fr-ML": WinLcid(0x340C),
    "ar-AE": WinLcid(0x3801),
    # "en-ID": WinLcid(0x3809),  # reserved
    "es-UY": WinLcid(0x380A),
    "fr-MA": WinLcid(0x380C),
    "ar-BH": WinLcid(0x3C01),
    "en-HK": WinLcid(0x3C09),
    "es-PY": WinLcid(0x3C0A),
    "fr-HT": WinLcid(0x3C0C),
    "ar-QA": WinLcid(0x4001),
    "en-IN": WinLcid(0x4009),
    "es-BO": WinLcid(0x400A),
    # "ar-Ploc-SA": WinLcid(0x4401),  # reserved
    "en-MY": WinLcid(0x4409),
    "es-SV": WinLcid(0x440A),
    # "ar-145": WinLcid(0x4801),  # reserved
    "en-SG": WinLcid(0x4809),
    "es-HN": WinLcid(0x480A),
    "en-AE": WinLcid(0x4C09),
    "es-NI": WinLcid(0x4C0A),
    # "en-BH": WinLcid(0x5009),  # reserved
    "es-PR": WinLcid(0x500A),
    # "en-EG": WinLcid(0x5409),  # reserved
    "es-US": WinLcid(0x540A),
    # "en-JO": WinLcid(0x5809),  # reserved
    # "es-419": WinLcid(0x580A),  # reserved
    # "en-KW": WinLcid(0x5C09),  # reserved
    "es-CU": WinLcid(0x5C0A),
    # "en-TR": WinLcid(0x6009),  # reserved
    # "en-YE": WinLcid(0x6409),  # reserved
    "bs-Cyrl": WinLcid(0x641A),
    "bs-Latn": WinLcid(0x681A),
    "sr-Cyrl": WinLcid(0x6C1A),
    "sr-Latn": WinLcid(0x701A),
    "smn": WinLcid(0x703B),
    "az-Cyrl": WinLcid(0x742C),
    "sms": WinLcid(0x743B),
    "zh": WinLcid(0x7804),
    "nn": WinLcid(0x7814),
    "bs": WinLcid(0x781A),
    "az-Latn": WinLcid(0x782C),
    "sma": WinLcid(0x783B),
    # "kk-Cyrl": WinLcid(0x783F),  # reserved
    "uz-Cyrl": WinLcid(0x7843),
    "mn-Cyrl": WinLcid(0x7850),
    "iu-Cans": WinLcid(0x785D),
    "tzm-Tfng": WinLcid(0x785F),
    "zh-Hant": WinLcid(0x7C04),
    "nb": WinLcid(0x7C14),
    "sr": WinLcid(0x7C1A),
    "tg-Cyrl": WinLcid(0x7C28),
    "dsb": WinLcid(0x7C2E),
    "smj": WinLcid(0x7C3B),
    # "kk-Latn": WinLcid(0x7C3F),  # reserved
    "uz-Latn": WinLcid(0x7C43),
    "pa-Arab": WinLcid(0x7C46),
    "mn-Mong": WinLcid(0x7C50),
    "sd-Arab": WinLcid(0x7C59),
    "chr-Cher": WinLcid(0x7C5C),
    "iu-Latn": WinLcid(0x7C5D),
    "tzm-Latn": WinLcid(0x7C5F),
    "ff-Latn": WinLcid(0x7C67),
    "ha-Latn": WinLcid(0x7C68),
    "ku-Arab": WinLcid(0x7C92),
    # "fr-015": WinLcid(0xE40C),  # reserved
}


# Gettext-style script designator words mapped to ISO 15924 script codes.
# This is not the full ISO 15924 table - it only contains the words that can
# hit entries in _LCID_TAGS above. Extend it as needed.
_SCRIPT_WORDS: dict[str, str] = {
    "latin": "Latn",
    "cyrillic": "Cyrl",
    "arabic": "Arab",
}


def lookup(lang: PoLang) -> WinLcid:
    """
    Resolve a PO file language to its Windows language identifier.

    :param lang: The PO file language.
    :return: The Windows language identifier for the language.
    :raises KeyError: If the language has no transcribed mapping.
    """
    if lang.variant is None:
        segments = [lang.language]
        if lang.country is not None:
            segments.append(lang.country)
        return _LCID_TAGS["-".join(segments)]

    # YYC MARK: PoLang's variant slot may hold either a script designator or a
    # genuine variant (Gettext semantics), while MS-LCID language tags place
    # scripts and variants at different positions with different vocabularies
    # ('cyrillic' != 'Cyrl'), so the conversion cannot be done mechanically.
    # Candidate matching is done here as a workaround: the variant position is
    # tried first, then the script position via _SCRIPT_WORDS (which is not
    # the full ISO 15924 table, only the words that hit entries above).
    key = f"{lang.language}-{lang.country}-{lang.variant}"
    if key in _LCID_TAGS:
        return _LCID_TAGS[key]
    script = _SCRIPT_WORDS.get(lang.variant)
    if script is not None:
        key = f"{lang.language}-{script}-{lang.country}"
        if key in _LCID_TAGS:
            return _LCID_TAGS[key]
    raise KeyError(str(lang))
