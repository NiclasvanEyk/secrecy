import json

import click
from rich.console import Console
from rich.table import Table
from secrecy import Secret
from secrecy._internals.source.registry import SourceRegistry
from secrecy.exception import SecrecyError

from secrecy_cli._internals.config.discovery import resolve_config
from secrecy_cli._internals.exceptions import exit_err
from secrecy_cli._internals.inspect import infer_source_type
from secrecy_cli._internals.io import OutputFormat
from secrecy_cli._internals.secrets.discovery import discover_secrets_in
from secrecy_cli._internals.utils import enum_type


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
    """Show all secrets discovered by the CLI.

    You can configure several modules to be scanned for secrets.
    """
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
    table.add_column("Type")
    table.add_column("Source")

    default = SourceRegistry.global_instance().default_source

    for secret in secrets:
        source_type = infer_source_type(secret)
        table.add_row(
            secret.definition().name,
            secret.definition().shape.__name__,
            # TODO: dynamic[unknown] for unknowns, dynamic[secrecy-aws:boto3] for known values based on env
            # TODO: If we notice a driver that could not be discovered, paint it red
            f"{source_type.__module__}.{source_type.__qualname__}"
            if source_type is not None
            else f"[gray50]{default or 'default'}",
        )

    console = Console()
    console.print(table)


def show_json(secrets: list[Secret]) -> None:
    serialized = json.dumps(
        [
            {
                "name": secret.definition().name,
                "type": secret.definition().shape.__name__,
                "source": "unresolved",
            }
            for secret in secrets
        ]
    )
    click.echo(serialized)
