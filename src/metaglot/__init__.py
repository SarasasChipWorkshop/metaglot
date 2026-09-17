import logging
import sys
from argparse import ArgumentParser
from .cmds import run, register, parse


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

    parser = ArgumentParser(
        prog="metaglot",
        description="A command-line tool that unifies localization metadata for applications shipped on multiple platforms.",
    )
    register(parser)
    args = vars(parser.parse_args())
    opts = parse(args)

    try:
        run(opts)
    except Exception as e:
        logging.fatal("Runtime error: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
