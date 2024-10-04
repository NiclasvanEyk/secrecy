from argparse import ArgumentParser
from importlib import import_module
from pkgutil import iter_modules

import secrecy_file.cli.commands as commands_module


def main() -> None:
    cli = ArgumentParser()

    commands = cli.add_subparsers(title="commands")
    for _, name, _ in iter_modules(commands_module.__path__):
        module = import_module(f"secrecy_file.cli.commands.{name}")
        command = commands.add_parser(name, help=module.__doc__)
        configure = getattr(module, "configure", None)
        if callable(configure):
            configure(command)

        execute = getattr(module, "execute", None)
        if callable(execute):
            command.set_defaults(func=execute)

    args = cli.parse_args()
    args.func(args)
