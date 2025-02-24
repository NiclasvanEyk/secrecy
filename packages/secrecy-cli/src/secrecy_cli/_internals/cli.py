import click

from secrecy_cli._internals.commands.drivers import drivers
from secrecy_cli._internals.commands.init import init
from secrecy_cli._internals.commands.list import list_command
from secrecy_cli._internals.commands.retrieve import retrieve
from secrecy_cli._internals.commands.sources import sources


@click.group()
def cli():
    """Manage your applications secrets from the command line."""


def main():
    cli.add_command(drivers)
    cli.add_command(init)
    cli.add_command(list_command)
    cli.add_command(retrieve)
    cli.add_command(sources)
    cli()
