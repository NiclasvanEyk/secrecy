import os

from secrecy.exception import MissingEnvironmentVariableError


def require_env_var(
    prefix: str,
    secret_name: str,
    unprefix_variable_name: str,
) -> str:
    environment_variable_name = f"{prefix}_{unprefix_variable_name}"
    value = os.environ.get(environment_variable_name)
    if value is None:
        raise MissingEnvironmentVariableError(
            environment_variable_name=environment_variable_name,
            secret_name=secret_name,
        )

    return value


def get_env_var(
    prefix: str,
    unprefix_variable_name: str,
    default: str,
) -> str:
    environment_variable_name = f"{prefix}_{unprefix_variable_name}"
    value = os.environ.get(environment_variable_name)
    return value if value is not None else default
