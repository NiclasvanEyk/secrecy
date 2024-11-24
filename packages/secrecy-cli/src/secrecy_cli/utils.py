from enum import StrEnum

import click


def enum_type(enum_cls: type[StrEnum]) -> click.Choice:
    return click.Choice(tuple([member.value for member in enum_cls]))
