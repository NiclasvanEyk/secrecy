import importlib
import os
from dataclasses import dataclass
from typing import Any


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
        raise Exception(
            f"Failed to infer driver. Set the {driver_env_var_name} to a valid and installed secrecy driver name!"
        )

    # Find the python function that will build the thing that fetches our secrets
    driver_module_specifier = {
        "aws-boto3": "secrecy_aws.drivers:boto3",
        "docker": "secrecy_docker.drivers:docker",
        "encrypted-file": "secrecy_file.drivers:encrypted_file",
        "environment": "secrecy_environment.drivers:environment",
        "google-cloud": "secrecy_google_cloud.drivers:secret_manager_sync",
        "onepassword-sdk": "secrecy_onepassword.drivers:sdk",
    }.get(driver)
    if driver_module_specifier is None:
        raise Exception(
            f"Unknown secrecy driver: '{driver_module_specifier}' for secret '{name}'"
        )
    setup_module_path, setup_function_name = driver_module_specifier.split(":")
    setup_module = importlib.import_module(setup_module_path)
    setup_driver = getattr(setup_module, setup_function_name, None)
    if setup_driver is None:
        raise Exception(
            f"Module {setup_module_path} does not contain an '{setup_function_name}' object"
        )

    if not callable(setup_driver):
        raise Exception(f"{driver_module_specifier} is not callable")

    # Actually build the thing
    return setup_driver, ResolvedSourceMeta(
        prefix=prefix,
        name=name,
        driver_module_specifier=driver_module_specifier,
    )
