import re
from typing import ClassVar, Optional
import langcodes
import pycountry


class PoLang:
    """
    Represents a valid Gettext PO file Language field value.

    Supported formats:
        ll              - ISO 639 language code (2 or 3 letters, lowercase)
        ll_CC           - language code + ISO 3166 country code (uppercase)
        ll_CC@variant   - language code + country code + variant (lowercase)

    Examples:
        PoLang("en")            # valid
        PoLang("zh_CN")         # valid
        PoLang("sr_Cyrl")       # valid (3-letter language code)
        PoLang("de_DE@euro")    # invalid (@euro is not a valid variant)
        PoLang("EN")            # invalid (language code must be lowercase)
    """

    __PATTERN: ClassVar[re.Pattern] = re.compile(
        r"^(?P<language>[a-z]{2,3})"
        r"(?:_(?P<country>[A-Z]{2})"
        r"(?:@(?P<variant>[a-z][a-z0-9-]*))?"
        r")?$"
    )

    __language_code: str
    """ISO 639 two-letter or three-letter language code (lowercase)."""
    __country_code: Optional[str]
    """ISO 3166 two-letter country code (uppercase) or no presented."""
    __variant: Optional[str]
    """The variant designator.
    The variant designator (lowercase) can be a script designator, 
    such as ‘latin’ or ‘cyrillic’.
    """

    def __init__(self, value: str):
        match = self.__PATTERN.match(value)
        if not match:
            raise ValueError(
                f"Invalid Language field format: {value!r}. "
                f"Expected 'll', 'll_CC' or 'll_CC@variant'"
            )

        self.__language_code = match.group("language")
        self.__country_code = match.group("country")  # may be None
        self.__variant = match.group("variant")  # may be None

        self.__validate_language(self.__language_code)
        if self.__country_code:
            self.__validate_country(self.__country_code)

    # region: Internal validation helpers

    @staticmethod
    def __validate_language(language_code: str) -> None:
        """Validate the language code as an ISO 639 code using pycountry."""
        lang = pycountry.languages.get(alpha_2=language_code)
        if lang is None:
            lang = pycountry.languages.get(alpha_3=language_code)
        if lang is None:
            raise ValueError(f"Invalid language code: {language_code!r}")

    @staticmethod
    def __validate_country(country_code: str) -> None:
        """Validate the country code as an ISO 3166 alpha-2 code using pycountry."""
        country = pycountry.countries.get(alpha_2=country_code)
        if country is None:
            raise ValueError(f"Invalid country code: {country_code!r}")

    # endregion

    # region: Properties

    @property
    def language(self) -> str:
        """The lowercase language code."""
        return self.__language_code

    @property
    def country(self) -> str | None:
        """The uppercase country code, or None if not specified."""
        return self.__country_code

    @property
    def variant(self) -> str | None:
        """The lowercase variant identifier, or None if not specified."""
        return self.__variant

    @property
    def value(self) -> str:
        """The canonical string representation, rebuilt from the components."""
        result = self.__language_code
        if self.__country_code is not None:
            result += f"_{self.__country_code}"
        if self.__variant is not None:
            result += f"@{self.__variant}"
        return result

    # endregion

    # region: Object methods

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"PoLang({self.value!r})"

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, PoLang):
            return NotImplemented
        return (
            self.__language_code == other.__language_code
            and self.__country_code == other.__country_code
            and self.__variant == other.__variant
        )

    def __hash__(self) -> int:
        return hash((self.__language_code, self.__country_code, self.__variant))

    # endregion


class DesktopLang:
    """
    Represents a freedesktop.org desktop entry locale, i.e. the ``LOCALE``
    postfix of a localized key (see the Desktop Entry Specification,
    section 5 "Localized values for keys").

    Supported formats:
        ll              - ISO 639 language code (2 or 3 letters, lowercase)
        ll_CC           - language code + ISO 3166 country code (uppercase)
        ll@modifier     - language code + modifier
        ll_CC@modifier  - language code + country code + modifier

    The ``.ENCODING`` part of the specification's grammar is deliberately
    not modeled: it is ignored when matching locales and never written by
    real world desktop entry files.

    Examples:
        DesktopLang("en")          # valid
        DesktopLang("zh_CN")       # valid
        DesktopLang("sr@Latn")     # valid (modifier without country)
        DesktopLang("sr_RS@latin") # valid
        DesktopLang("EN")          # invalid (language code must be lowercase)
    """

    __PATTERN: ClassVar[re.Pattern] = re.compile(
        r"^(?P<language>[a-z]{2,3})"
        r"(?:_(?P<country>[A-Z]{2}))?"
        r"(?:@(?P<modifier>[a-zA-Z][a-zA-Z0-9-]*))?$"
    )

    __language_code: str
    """ISO 639 two-letter or three-letter language code (lowercase)."""
    __country_code: Optional[str]
    """ISO 3166 two-letter country code (uppercase) or no presented."""
    __modifier: Optional[str]
    """The modifier designator, such as 'latin' or 'Latn'."""

    def __init__(self, value: str):
        match = self.__PATTERN.match(value)
        if not match:
            raise ValueError(
                f"Invalid desktop locale format: {value!r}. "
                f"Expected 'll', 'll_CC', 'll@modifier' or 'll_CC@modifier'"
            )

        self.__language_code = match.group("language")
        self.__country_code = match.group("country")  # may be None
        self.__modifier = match.group("modifier")  # may be None

        self.__validate_language(self.__language_code)
        if self.__country_code:
            self.__validate_country(self.__country_code)

    # region: Internal validation helpers

    @staticmethod
    def __validate_language(language_code: str) -> None:
        """Validate the language code as an ISO 639 code using pycountry."""
        lang = pycountry.languages.get(alpha_2=language_code)
        if lang is None:
            lang = pycountry.languages.get(alpha_3=language_code)
        if lang is None:
            raise ValueError(f"Invalid language code: {language_code!r}")

    @staticmethod
    def __validate_country(country_code: str) -> None:
        """Validate the country code as an ISO 3166 alpha-2 code using pycountry."""
        country = pycountry.countries.get(alpha_2=country_code)
        if country is None:
            raise ValueError(f"Invalid country code: {country_code!r}")

    # endregion

    # region: Properties

    @property
    def language(self) -> str:
        """The lowercase language code."""
        return self.__language_code

    @property
    def country(self) -> str | None:
        """The uppercase country code, or None if not specified."""
        return self.__country_code

    @property
    def modifier(self) -> str | None:
        """The modifier identifier, or None if not specified."""
        return self.__modifier

    @property
    def value(self) -> str:
        """The canonical string representation, rebuilt from the components."""
        result = self.__language_code
        if self.__country_code is not None:
            result += f"_{self.__country_code}"
        if self.__modifier is not None:
            result += f"@{self.__modifier}"
        return result

    # endregion

    # region: Object methods

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"DesktopLang({self.value!r})"

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, DesktopLang):
            return NotImplemented
        return (
            self.__language_code == other.__language_code
            and self.__country_code == other.__country_code
            and self.__modifier == other.__modifier
        )

    def __hash__(self) -> int:
        return hash((self.__language_code, self.__country_code, self.__modifier))

    # endregion


class AppStreamLang:
    """
    Represents a BCP 47 language tag, as required by the ``xml:lang``
    attribute values of AppStream XML files.

    Validation and serialization are delegated to the core of the
    ``langcodes`` library (without its optional ``data`` extra). The whole
    of BCP 47 is therefore accepted, and subtags are checked against the
    IANA registry: ``zh-CN``, ``sr-Latn-RS`` and ``ca-ES-valencia`` are
    valid, while ``jp`` and the unregistered variant ``euro`` are not.

    Tags are case-insensitive per BCP 47, and close-but-nonstandard
    spellings are normalized: ``zh-cn`` and ``zh_CN`` both canonicalize
    to ``zh-CN``.

    Deliberate usage policy: MetaGlot only parses, validates and
    serializes tags through this class. It never calls
    ``langcodes.standardize_tag`` nor enables macro language collapsing,
    so an emitted ``xml:lang`` is always a faithful hyphenation of its
    Gettext source tag - no script injection, no redundant-script
    removal, no macrolanguage folding.

    Examples:
        AppStreamLang("zh-CN")        # valid
        AppStreamLang("sr-Latn-RS")   # valid
        AppStreamLang("zh_CN")        # valid, normalizes to "zh-CN"
        AppStreamLang("de-DE-euro")   # invalid (unregistered variant)
        AppStreamLang("jp")           # invalid (not a language code)
    """

    __lang: langcodes.Language
    """The underlying langcodes language object."""

    def __init__(self, value: str):
        try:
            lang = langcodes.Language.get(value)
        except ValueError as exc:
            raise ValueError(
                f"Invalid BCP 47 language tag: {value!r}. ({exc})"
            ) from exc
        if not lang.is_valid():
            raise ValueError(f"Invalid BCP 47 language tag: {value!r}")
        self.__lang = lang

    # region: Properties

    @property
    def language(self) -> Optional[str]:
        """The lowercase language subtag, or None if unspecified."""
        return self.__lang.language

    @property
    def script(self) -> Optional[str]:
        """The title-case script subtag, or None if not specified."""
        return self.__lang.script

    @property
    def territory(self) -> Optional[str]:
        """The uppercase territory subtag, or None if not specified."""
        return self.__lang.territory

    @property
    def variant(self) -> Optional[str]:
        """The first variant subtag, or None if not specified."""
        variants = self.__lang.variants or []
        return variants[0] if variants else None

    @property
    def value(self) -> str:
        """The canonical string form, in BCP 47 conventional casing."""
        return str(self.__lang)

    # endregion

    # region: Object methods

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"AppStreamLang({self.value!r})"

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, AppStreamLang):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    # endregion


class WinLcid:
    """
    Represents a Windows language identifier (LANGID), the 2-byte language
    component of a Windows LCID (see [MS-LCID] section 2.2).

    A LANGID combines a 10-bit primary language identifier and a 6-bit
    sublanguage identifier. This is the value used by the LANGUAGE statement of
    RC STRINGTABLE resources and the "Translation" value of VERSIONINFO
    resources, so unlike a full 4-byte LCID it carries no sort identifier.

    The value is only loosely validated: it must fit into 2 bytes, but it is
    not checked against the identifiers actually assigned by Microsoft.

    Examples:
        WinLcid(0x0409)      # valid
        WinLcid(0x7C14)      # valid
        WinLcid(0x10000)     # invalid (exceeds the 2-byte range)
    """

    __value: int
    """The LANGID value, from 0x0000 to 0xFFFF."""

    def __init__(self, value: int):
        if not 0 <= value <= 0xFFFF:
            raise ValueError(
                f"Invalid language identifier value: {value:#x}. "
                f"Expected a 2-byte integer between 0x0000 and 0xFFFF"
            )
        self.__value = value

    @classmethod
    def from_parts(cls, primary: int, sublanguage: int) -> "WinLcid":
        """
        Create a language identifier from a primary/sublanguage pair, as used
        by the two-number form of the RC LANGUAGE statement.

        :param primary: The primary language identifier (10 bits).
        :param sublanguage: The sublanguage identifier (6 bits).
        :return: The combined language identifier.
        """
        if not 0 <= primary <= 0x3FF:
            raise ValueError(
                f"Invalid primary language identifier: {primary:#x}. "
                f"Expected a 10-bit integer between 0x000 and 0x3FF"
            )
        if not 0 <= sublanguage <= 0x3F:
            raise ValueError(
                f"Invalid sublanguage identifier: {sublanguage:#x}. "
                f"Expected a 6-bit integer between 0x00 and 0x3F"
            )
        return cls((sublanguage << 10) | primary)

    # region: Properties

    @property
    def value(self) -> int:
        """The LANGID value as an integer."""
        return self.__value

    @property
    def primary(self) -> int:
        """The primary language identifier (the low-order 10 bits)."""
        return self.__value & 0x3FF

    @property
    def sublanguage(self) -> int:
        """The sublanguage identifier (the high-order 6 bits)."""
        return self.__value >> 10

    # endregion

    # region: Object methods

    def __str__(self) -> str:
        return f"0x{self.__value:04X}"

    def __repr__(self) -> str:
        return f"WinLcid(0x{self.__value:04X})"

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        if not isinstance(other, WinLcid):
            return NotImplemented
        return self.__value == other.__value

    def __hash__(self) -> int:
        return hash(self.__value)

    # endregion
