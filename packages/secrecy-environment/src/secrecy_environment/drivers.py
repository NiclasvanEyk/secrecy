from secrecy_environment.sources.environment.sync import (
    EnvironmentVariablesSecretsSource,
)


def environment(prefix: str, name: str) -> EnvironmentVariablesSecretsSource:
    return EnvironmentVariablesSecretsSource(prefix)
