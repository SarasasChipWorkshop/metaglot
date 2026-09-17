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
