import logging
import sys
from .cli import parse
from .cmds import run


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    opts = parse()

    try:
        run(opts)
    except Exception as e:
        logging.fatal("Runtime error: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
