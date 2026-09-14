from argparse import ArgumentParser
from pathlib import Path


def create_argparser() -> ArgumentParser:
    """
    Create MetaGlot argument parser.

    :return: The built argument parser.
    """
    parser = ArgumentParser(
        prog="metaglot",
        description="A command-line tool that unifies localization metadata for applications shipped on multiple platforms.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    rc = commands.add_parser(
        "rc",
        help="Commands for Windows RC resource files.",
    )
    rc_commands = rc.add_subparsers(dest="rc_command", required=True)

    rc_pot = rc_commands.add_parser(
        "pot",
        help="Generate a POT template from a string manifest.",
    )
    rc_pot.add_argument(
        "-m",
        "--manifest",
        dest="manifest",
        action="store",
        type=Path,
        required=True,
        help="The path to the string manifest file.",
        metavar="FILE",
    )
    rc_pot.add_argument(
        "-o",
        "--output",
        dest="output",
        action="store",
        type=Path,
        required=True,
        help="The path of the POT file to write.",
        metavar="FILE",
    )

    rc_render = rc_commands.add_parser(
        "render",
        help="Render a user-provided template with manifest data and PO translations.",
    )
    rc_render.add_argument(
        "-m",
        "--manifest",
        dest="manifest",
        action="store",
        type=Path,
        required=True,
        help="The path to the string manifest file.",
        metavar="FILE",
    )
    rc_render.add_argument(
        "-p",
        "--po",
        dest="po",
        action="extend",
        nargs="+",
        type=Path,
        required=True,
        help="The PO files to read, each may be a glob pattern.",
        metavar="GLOB",
    )
    rc_render.add_argument(
        "-t",
        "--template",
        dest="template",
        action="store",
        type=Path,
        required=True,
        help="The path to the user-provided Liquid template.",
        metavar="FILE",
    )
    rc_render.add_argument(
        "-o",
        "--output",
        dest="output",
        action="store",
        type=Path,
        required=True,
        help="The path of the rendered file to write.",
        metavar="FILE",
    )

    return parser
