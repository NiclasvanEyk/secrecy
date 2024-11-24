import json

import click
from rich.console import Console
from rich.table import Table
from secrecy.exception import SecrecyError
from secrecy.secret import Secret

from secrecy_cli.config.discovery import resolve_config
from secrecy_cli.exceptions import exit_err
from secrecy_cli.inspect import infer_source_type
from secrecy_cli.io import OutputFormat
from secrecy_cli.secrets.discovery import discover_secrets_in
from secrecy_cli.utils import enum_type


@click.command(name="list")
@click.option(
    "--format",
    type=enum_type(OutputFormat),
    default=OutputFormat.TEXT,
    show_default=True,
)
@click.option(
    "--resolve",
    help="Resolve and construct environment-variable based secrets",
    default=False,
    is_flag=True,
    show_default=True,
)
def list_command(format: OutputFormat, resolve: bool):
    """Fetch a secret from the specified source."""

    try:
        config = resolve_config()
        secrets = discover_secrets_in(config.secrets.modules)

        if format == OutputFormat.TEXT:
            show_text(secrets)
        elif format == OutputFormat.JSON:
            show_json(secrets)
    except SecrecyError as exception:
        exit_err(str(exception))


def show_text(secrets: list[Secret]) -> None:
    table = Table(box=None)
    table.add_column("Name")
    table.add_column("Driver")

    for secret in secrets:
        source_type = infer_source_type(secret)
        table.add_row(
            secret.name,
            f"{source_type.__module__}.{source_type.__qualname__}"
            if source_type is not None
            else "[gray50]dynamic",
        )

    console = Console()
    console.print(table)


def show_json(secrets: list[Secret]) -> None:
    serialized = json.dumps(
        [
            {
                "name": secret.name,
                "driver": "unresolved",
            }
            for secret in secrets
        ]
    )
    click.echo(serialized)
