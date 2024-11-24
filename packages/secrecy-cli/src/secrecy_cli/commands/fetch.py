import click
from secrecy.exception import SecrecyError
from secrecy.secret import Secret

from secrecy_cli.config.discovery import resolve_config
from secrecy_cli.secrets.discovery import discover_secrets_in


@click.command()
@click.argument("name")
def fetch(name: str):
    """Fetch a secret from the specified source."""

    try:
        config = resolve_config()
        secrets = discover_secrets_in(config.secrets.modules)
        secret = find_secret_by_name(name, secrets)

        click.echo(secret.values)
    except SecrecyError as exception:
        click.echo(click.style(str(exception), fg="red"), err=True)
        exit(1)


def find_secret_by_name(name: str, candidates: list[Secret]) -> Secret:
    matches = [secret for secret in candidates if secret.name == name]
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
