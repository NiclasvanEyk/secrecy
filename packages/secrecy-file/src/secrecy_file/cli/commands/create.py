"""
initialize a new encrypted file
"""

from argparse import ArgumentParser, Namespace


def configure(command: ArgumentParser) -> None:
    command.add_argument("name", help="name of the file in the secrets/ directory")


def execute(args: Namespace) -> None:
    print(f"Creating: {args.name}")
