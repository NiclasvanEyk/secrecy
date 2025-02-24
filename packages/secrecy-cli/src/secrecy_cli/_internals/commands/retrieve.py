import click
from secrecy import Secret
from secrecy.exception import SecrecyError

from secrecy_cli._internals.config.discovery import resolve_config
from secrecy_cli._internals.secrets.discovery import discover_secrets_in


@click.command()
@click.argument("name")
def retrieve(name: str):
    """Fetch a secret from the specified source."""
    try:
        config = resolve_config()
        secrets = discover_secrets_in(config.secrets.modules)
        secret = find_secret_by_name(name, secrets)

        click.echo(secret.retrieve())
    except SecrecyError as exception:
        click.echo(click.style(str(exception), fg="red"), err=True)
        exit(1)


def find_secret_by_name(name: str, candidates: list[Secret]) -> Secret:
    matches = [secret for secret in candidates if secret.definition().name == name]
    if len(matches) < 1:
        click.echo(
            click.style(f"Failed to find a secret called '{name}'", fg="red"),
            err=True,
        )
        exit(1)

    if len(matches) > 1:
        modules = ", ".join([secret.__module__ for secret in matches])
        click.echo(
            click.style(
                f"Multiple secrets are called '{name}'. Found in {modules}",
                fg="red",
            ),
            err=True,
        )
        exit(1)

    return matches[0]
