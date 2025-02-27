import json

import click
from rich.console import Console
from rich.table import Table
from secrecy._internals.source.registry import SourceRegistry
from secrecy.exception import SecrecyError

from secrecy_cli._internals.config.discovery import resolve_config
from secrecy_cli._internals.exceptions import exit_err
from secrecy_cli._internals.io import OutputFormat
from secrecy_cli._internals.secrets.discovery import discover_secrets_in
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
        # This will register all sources as a side effect
        config = resolve_config()
        _ = discover_secrets_in(config.secrets.modules)

        registry = SourceRegistry.global_instance()

        sources = []
        for source_name, source_type in registry._implicit_factories.items():
            sources.append((source_name, source_type))
        for source_name, factory in registry._factories.items():
            # Can be tried to be inferred frmo the return type
            sources.append((source_name, "Unknown"))

        if format == OutputFormat.TEXT:
            show_text(sources, registry.default_source)
        elif format == OutputFormat.JSON:
            show_json(sources, registry.default_source)
    except SecrecyError as exception:
        exit_err(str(exception))


def full_qualname(t: type) -> str:
    return f"{t.__module__}.{t.__qualname__}"


def show_text(sources: list[tuple[str, str | type]], default: str | None) -> None:
    table = Table(box=None)
    table.add_column("Source")
    table.add_column("Type")
    table.add_column("Default")

    for source_name, source_type in sources:
        table.add_row(
            source_name,
            source_type if isinstance(source_type, str) else full_qualname(source_type),
            "yes" if source_name == default else "",
        )

    console = Console()
    console.print(table)


def show_json(sources: list[tuple[str, str | type]], default: str | None) -> None:
    serialized = json.dumps(
        [
            {
                "name": source_name,
                "type": source_type
                if isinstance(source_type, str)
                else full_qualname(source_type),
                "default": source_name == default,
            }
            for source_name, source_type in sources
        ]
    )
    click.echo(serialized)
