"""
Internal use only.

This module is not considered for any backwards compatibility or semver
guarantees. This module will have breaking changes in minor or even patch
versions!
"""

import importlib
import os
from dataclasses import dataclass
from typing import Any

from secrecy.drivers import WELL_KNOWN_DRIVERS
from secrecy.exception import SecrecyError


@dataclass
class ResolvedSourceMeta:
    prefix: str
    name: str
    driver_module_specifier: str


def resolve_source_factory(name: str) -> tuple[Any, ResolvedSourceMeta]:
    prefix = f"SECRECY_{name.upper()}"

    # Find out how to build the thing that fetches our secrets
    driver_env_var_name = f"{prefix}_DRIVER"
    driver = os.getenv(driver_env_var_name)
    if driver is None:
        raise SecrecyError(
            f"Failed to infer driver. Set the {driver_env_var_name} to a valid and installed secrecy driver name!"
        )

    # Find the python function that will build the thing that fetches our secrets
    driver_module_specifier = WELL_KNOWN_DRIVERS.get(driver)
    if driver_module_specifier is None:
        raise SecrecyError(
            f"Unknown secrecy driver: '{driver_module_specifier}' for secret '{name}'"
        )
    setup_module_path, setup_function_name = driver_module_specifier.split(":")
    setup_module = importlib.import_module(setup_module_path)
    setup_driver = getattr(setup_module, setup_function_name, None)
    if setup_driver is None:
        raise SecrecyError(
            f"Module {setup_module_path} does not contain an '{setup_function_name}' object"
        )

    if not callable(setup_driver):
        raise SecrecyError(f"{driver_module_specifier} is not callable")

    # Actually build the thing
    return setup_driver, ResolvedSourceMeta(
        prefix=prefix,
        name=name,
        driver_module_specifier=driver_module_specifier,
    )
