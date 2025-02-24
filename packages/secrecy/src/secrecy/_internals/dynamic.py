import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from secrecy._internals.dotted_path import import_dotted_path
from secrecy._internals.drivers import Driver, discover_drivers
from secrecy.exception import SecrecyError


@dataclass
class ResolvedSourceMeta:
    prefix: str
    """A common prefix for all environment variables relevant to this secret.

    Example: 'SECRECY_DATABASE_CREDENTIALS'
    """

    name: str
    """The lowercase name of the secret.

    Example: 'database_credentials'
    """

    driver: Driver
    """The resolved driver object, that at this point is proven to exist."""


def resolve_dynamic_source_factory(
    name: str,
) -> tuple[Callable[[str], Any], ResolvedSourceMeta]:
    prefix = f"SECRECY_{name.upper()}"

    # First we resolve the driver name
    driver_env_var_name = f"{prefix}_DRIVER"
    driver_name = os.getenv(driver_env_var_name)
    if driver_name is None or driver_name.strip() == "":
        raise SecrecyError(
            f"Failed to infer driver. Set the {driver_env_var_name} to a secrecy driver name!"
        )

    # then we resolve a pointer to the source_factory
    drivers = discover_drivers()
    matching_drivers = [driver for driver in drivers if driver.name == driver_name]
    if len(matching_drivers) <= 0:
        raise SecrecyError(f"Could not find a matching driver named {driver_name}!")
    driver = matching_drivers[0]

    # finally we import the source_factory, which contains the knowledge to
    # resolve further configuration from the environment, as well as actually
    # building a secret source from the configuration.
    _, source_factory = import_dotted_path(driver.dotted_path)
    if not callable(source_factory):
        raise SecrecyError(f"{driver_name} is not callable")

    # We return this tuple construct, to re-use this logic across sync and async APIs.
    # For the former, we want to check if the function, once called actually instantiated a `Source` instance,
    # and for the latter it should either be an `AsyncSource`, or a Coroutine or other Awaitable that then
    # after awaiting resolves to an `AsyncSource`.
    return source_factory, ResolvedSourceMeta(prefix=prefix, name=name, driver=driver)
