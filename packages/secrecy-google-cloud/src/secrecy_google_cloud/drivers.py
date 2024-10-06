from google.cloud.secretmanager import SecretManagerServiceClient
from secrecy.autoresolve.environment import (
    optional_environment_variable,
    require_environment_variable,
)

from secrecy_google_cloud.sources.secret_manager.sync import SecretManagerSecretSource


def secret_manager_sync(prefix: str, secret_name: str) -> SecretManagerSecretSource:
    return SecretManagerSecretSource(
        client=SecretManagerServiceClient(),
        project_id=require_environment_variable(prefix, secret_name, "PROJECT_ID"),
        secret_name=secret_name,
        secret_version=optional_environment_variable(
            prefix, secret_name, "VERSION", "latest"
        ),
    )
