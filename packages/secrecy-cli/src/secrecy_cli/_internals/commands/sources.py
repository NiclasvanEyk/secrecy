import json

import click
from rich.console import Console
from rich.table import Table
from secrecy._internals.drivers import Driver
from secrecy._internals.source.registry import SourceRegistry
from secrecy.exception import SecrecyError

from secrecy_cli._internals.exceptions import exit_err
from secrecy_cli._internals.io import OutputFormat
from secrecy_cli._internals.utils import enum_type


@click.command()
@click.option(
    "--format",
    type=enum_type(OutputFormat),
    default=OutputFormat.TEXT,
    show_default=True,
)
def sources(format: OutputFormat):
    """Show all discovered secret sources."""
    try:
        registry = SourceRegistry.global_instance()

        if format == OutputFormat.TEXT:
            show_text(drivers)
        elif format == OutputFormat.JSON:
            show_json(drivers)
    except SecrecyError as exception:
        exit_err(str(exception))


def show_text(drivers: list[Driver]) -> None:
    table = Table(box=None)
    table.add_column("Source")
    table.add_column("Location")

    for driver in drivers:
        table.add_row(driver.name, f"{driver.module}:{driver.member}")

    console = Console()
    console.print(table)


def show_json(drivers: list[Driver]) -> None:
    serialized = json.dumps(
        [
            {
                "driver": driver.name,
                "location": f"{driver.module}:{driver.member}",
            }
            for driver in drivers
        ]
    )
    click.echo(serialized)
