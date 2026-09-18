import logging
from collections.abc import Iterable
from pathlib import Path
from typing import Protocol

from liquid import Environment, StrictUndefined
from liquid.exceptions import LiquidError


class RenderContext(Protocol):
    """The interface required of a top-level rendering context.

    A render context routes template variable lookups dynamically (Liquid
    performs item access only), and enumerates its variable names the same
    way the ``dict`` constructor does, so an instance can be passed to
    ``BoundTemplate.render`` directly.
    """

    def keys(self) -> Iterable[str]:
        """Return the names of the top-level template variables."""
        ...

    def __getitem__(self, key: str) -> object:
        """Return the value of the named top-level template variable."""
        ...


def create_environment() -> Environment:
    """Create a Liquid environment for rendering.

    The environment runs in strict mode: referencing a variable or a property
    that does not exist fails the render. No filters are registered; callers
    register what they need with the functions of the ``filters`` module.

    :return: The created environment.
    """
    return Environment(undefined=StrictUndefined)


def render(
    env: Environment,
    template_path: Path,
    context: RenderContext,
    output_path: Path,
) -> None:
    """Render a Liquid template and write the result to a file.

    The template is read as UTF-8. The rendered output is written as UTF-8
    using the system's native line endings.

    :param env: The environment to render with.
    :param template_path: The path of the template file.
    :param context: The top-level render context passed to the template.
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
        content = template.render(context)
    except LiquidError as exc:
        raise RuntimeError(
            f"failed to render template '{template_path}': {exc}"
        ) from exc

    output_path.write_text(content, encoding="utf-8")
    logging.info("Wrote rendered output to %s", output_path)
