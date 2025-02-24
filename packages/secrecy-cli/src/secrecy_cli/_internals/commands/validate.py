import json

import click
from rich.console import Console
from rich.table import Table
from secrecy import Secret
from secrecy._internals.drivers import discover_drivers
from secrecy.exception import SecrecyError

from secrecy_cli._internals.config.discovery import resolve_config
from secrecy_cli._internals.exceptions import exit_err
from secrecy_cli._internals.inspect import infer_source_type
from secrecy_cli._internals.io import OutputFormat
from secrecy_cli._internals.secrets.discovery import discover_secrets_in
from secrecy_cli._internals.utils import enum_type


@click.command()
@click.option(
    "--retrieve",
    help="Resolve and construct environment-variable based secrets",
    default=False,
    is_flag=True,
    show_default=True,
)
def list_command(retrieve: bool):
    """Validate the secret configurations."""
    try:
        config = resolve_config()
        secrets = discover_secrets_in(config.secrets.modules)
        drivers = discover_drivers()

        # TODO: Validate that drivers exist

        if retrieve:
            pass
            # TODO: retrieve each

    except SecrecyError as exception:
        exit_err(str(exception))
