import logging
import sys

from . import pot, render
from .cli import create_argparser


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    parser = create_argparser()
    args = parser.parse_args()

    try:
        if args.command == "rc":
            if args.rc_command == "pot":
                pot.generate(args.manifest, args.output)
            elif args.rc_command == "render":
                render.render(args.manifest, args.po, args.template, args.output)
    except (ValueError, RuntimeError) as exc:
        logging.fatal("%s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
