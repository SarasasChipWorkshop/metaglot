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
    env.add_filter("to_string", str)
    env.add_filter("format", str.format)
    env.add_filter("to_integer", int)
    env.add_filter("to_float", float)
    env.add_filter("is_integer", _is_integer)
    env.add_filter("is_float", _is_float)


def _rc_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def register_rc_specific_filters(env: Environment) -> None:
    env.add_filter("rc_escape", _rc_escape)
