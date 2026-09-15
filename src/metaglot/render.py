import logging
from pathlib import Path

from liquid import Environment, StrictUndefined
from liquid.exceptions import LiquidError


def create_environment() -> Environment:
    """Create a Liquid environment for rendering.

    The environment runs in strict mode: referencing a variable or a property
    that does not exist fails the render. No filters are registered; callers
    register what they need with the functions of the ``filters`` module.

    :return: The created environment.
    """
    return Environment(undefined=StrictUndefined)


def render(
    env: Environment, template_path: Path, context: dict, output_path: Path
) -> None:
    """Render a Liquid template and write the result to a file.

    The template is read as UTF-8. The rendered output is written as UTF-8
    using the system's native line endings.

    :param env: The environment to render with.
    :param template_path: The path of the template file.
    :param context: The top-level variables passed to the template.
    :param output_path: The path of the rendered file to write.
    :raises ValueError: If the template file does not exist.
    :raises RuntimeError: If the template cannot be read or rendered.
    """
    if not template_path.is_file():
        raise ValueError(f"template file not found: {template_path}")
    try:
        template_source = template_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"failed to read template '{template_path}': {exc}") from exc

    try:
        template = env.from_string(
            template_source, name=str(template_path), path=template_path
        )
        content = template.render(**context)
    except LiquidError as exc:
        raise RuntimeError(
            f"failed to render template '{template_path}': {exc}"
        ) from exc

    output_path.write_text(content, encoding="utf-8")
    logging.info("Wrote rendered output to %s", output_path)
