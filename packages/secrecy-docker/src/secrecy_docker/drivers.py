from pathlib import Path
from platform import system

from secrecy.autoresolve.environment import optional_environment_variable

from secrecy_docker.sources.environment.sync import (
    DockerSecretsSource,
)


def default_secrets_directory() -> str:
    return (
        "C:\\ProgramData\\Docker\\secrets" if system() == "Windows" else "/run/secrets"
    )


def docker(prefix: str, secret_name: str) -> DockerSecretsSource:
    secrets_directory = optional_environment_variable(
        prefix,
        "SECRETS_DIRECTORY",
        default_secrets_directory(),
    )

    return DockerSecretsSource(secret_name, Path(secrets_directory))
