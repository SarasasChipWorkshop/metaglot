from liquid import Environment


def _is_integer(s: str) -> bool:
    try:
        int(s)
        return True
    except (TypeError, ValueError):
        return False


def _is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


def register_general_filters(env: Environment) -> None:
    """Register the general-purpose Liquid filters available in every rendering.

    :param env: The environment to register the filters on.
    """
    env.add_filter("to_string", str)
    env.add_filter("format", str.format)
    env.add_filter("to_integer", int)
    env.add_filter("to_float", float)
    env.add_filter("is_integer", _is_integer)
    env.add_filter("is_float", _is_float)


def _rc_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def register_rc_filters(env: Environment) -> None:
    """Register the Liquid filters specific to Windows RC file rendering.

    :param env: The environment to register the filters on.
    """
    env.add_filter("rc_escape", _rc_escape)


def _desktop_escape(value: str) -> str:
    """Escape a desktop entry string value (see the Desktop Entry
    Specification, section 4 "Possible value types").

    Backslash, newline, carriage return and tab are escaped everywhere.
    Spaces are additionally escaped as ``\\s`` when leading or trailing,
    where parsers may trim them away.
    """
    core = (
        value.replace("\\", "\\\\")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    lstripped = core.lstrip(" ")
    leading = len(core) - len(lstripped)
    trailing = len(lstripped) - len(lstripped.rstrip(" "))
    return "\\s" * leading + lstripped.rstrip(" ") + "\\s" * trailing


def register_desktop_filters(env: Environment) -> None:
    """Register the Liquid filters specific to desktop entry file rendering.

    :param env: The environment to register the filters on.
    """
    env.add_filter("desktop_escape", _desktop_escape)


def _xml_escape(value: str) -> str:
    """Escape a string for use in XML text content or attribute values.

    The five predefined XML entities are produced: ``&`` becomes ``&amp;``,
    ``<`` becomes ``&lt;``, ``>`` becomes ``&gt;``, ``"`` becomes ``&quot;``
    and ``'`` becomes ``&apos;``.
    """
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def register_appstream_filters(env: Environment) -> None:
    """Register the Liquid filters specific to AppStream XML file rendering.

    :param env: The environment to register the filters on.
    """
    env.add_filter("xml_escape", _xml_escape)


def _json_escape(value: str) -> str:
    """Escape a string for use inside a JSON string literal.

    Like the other ``_escape`` filters, this escapes only and adds no
    surrounding quotes: ``"`` becomes ``\\"``, ``\\`` becomes ``\\\\``,
    newline, carriage return and tab become ``\\n``, ``\\r`` and ``\\t``,
    any other control character below 0x20 becomes its ``\\uXXXX`` form,
    and non-ASCII characters carry over unchanged.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return "".join(
        char if ord(char) >= 0x20 else f"\\u{ord(char):04X}" for char in escaped
    )


def register_msix_manifest_filters(env: Environment) -> None:
    """Register the Liquid filters for the MSIX manifest file rendering.

    :param env: The environment to register the filters on.
    """
    env.add_filter("xml_escape", _xml_escape)


def register_msix_resources_filters(env: Environment) -> None:
    """Register the Liquid filters for the MSIX resources file rendering.

    :param env: The environment to register the filters on.
    """
    env.add_filter("xml_escape", _xml_escape)
    env.add_filter("json_escape", _json_escape)


def _plist_strings_escape(value: str) -> str:
    """Escape a string for use inside an InfoPlist.strings value.

    The escape sequences of the strings file format are produced: ``\\``
    becomes ``\\\\``, ``"`` becomes ``\\"``, linefeed, carriage return and
    tab become ``\\n``, ``\\r`` and ``\\t``. Non-ASCII characters carry
    over unchanged, as strings files are UTF-8 by definition.
    """
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


def register_plist_info_filters(env: Environment) -> None:
    """Register the Liquid filters for the Info.plist file rendering.

    :param env: The environment to register the filters on.
    """
    env.add_filter("xml_escape", _xml_escape)


def register_plist_strings_filters(env: Environment) -> None:
    """Register the Liquid filters for the InfoPlist.strings file rendering.

    :param env: The environment to register the filters on.
    """
    env.add_filter("plist_strings_escape", _plist_strings_escape)
