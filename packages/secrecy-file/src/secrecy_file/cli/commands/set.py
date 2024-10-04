"""
set a value in the encrypted file
"""

from argparse import ArgumentParser


def configure(command: ArgumentParser) -> None:
    command.add_argument(
        "key", help="an identifier that is unique in the context of the file"
    )
    command.add_argument("value", help="the value associated with the key")
    command.add_argument("--name", help="name of the file in the secrets/ directory")
    command.add_argument("--password", help="password of the file")


def execute() -> None:
    pass
