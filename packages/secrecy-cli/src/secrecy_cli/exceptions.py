from typing import Never

import click


def exit_err(message: str) -> Never:
    click.echo(click.style(message, fg="red"), err=True)
    exit(1)
