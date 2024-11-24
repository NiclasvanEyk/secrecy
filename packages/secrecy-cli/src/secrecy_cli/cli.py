import click

from secrecy_cli.commands.fetch import fetch
from secrecy_cli.commands.list import list_command


@click.group()
def cli():
    pass


def main():
    cli.add_command(fetch)
    cli.add_command(list_command)
    cli()
