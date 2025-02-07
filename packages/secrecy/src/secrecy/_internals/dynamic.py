import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from secrecy._internals.dotted_path import import_dotted_path
from secrecy.exception import SecrecyError


@dataclass
class ResolvedSourceMeta:
    prefix: str
    name: str
    driver: str


def resolve_dynamic_source_factory(
    name: str,
) -> tuple[Callable[[str], Any], ResolvedSourceMeta]:
    prefix = f"SECRECY_{name.upper()}"

    # Find out how to build the thing that fetches our secrets
    driver_env_var_name = f"{prefix}_DRIVER"
    driver = os.getenv(driver_env_var_name)
    if driver is None:
        raise SecrecyError(
            f"Failed to infer driver. Set the {driver_env_var_name} to a valid and installed secrecy driver name!"
        )

    _, source_factory = import_dotted_path(driver)
    if not callable(source_factory):
        raise SecrecyError(f"{driver} is not callable")

    # We return this tuple construct, to re-use this logic across sync and async APIs.
    # For the former, we want to check if the function, once called actually instantiated a `Source` instance,
    # and for the latter it should either be an `AsyncSource`, or a Coroutine or other Awaitable that then
    # after awaiting resolves to an `AsyncSource`.
    return source_factory, ResolvedSourceMeta(prefix=prefix, name=name, driver=driver)
