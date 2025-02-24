from typing import override

from google.cloud.secretmanager import SecretManagerServiceClient
from secrecy import Definition, Source
from secrecy._internals.environment import (
    get_env_var,
    require_env_var,
)
from secrecy.serialization import serialize_from_string

from secrecy_google_cloud.sources.secret_manager.sync import SecretManagerSecretSource


class SecretManagerSource(Source):
    def __init__(
        self,
        client: SecretManagerServiceClient,
        project_id: str,
    ) -> None:
        super().__init__()
        self.client = client
        self.project_id = project_id

    @override
    def fetch[T](self, definition: Definition[T]) -> T:
        response = self.client.access_secret_version(
            name=self.resource_name(definition.name)
        )
        payload = response.payload.data.decode("UTF-8")
        return serialize_from_string(definition, payload)

    @override
    def validate[T](self, definition: Definition[T]) -> None:
        # TODO
        pass

    def resource_name(self, secret_name: str) -> str:
        # TODO: Make this parameterizable
        secret_version = "latest"
        return f"projects/{self.project_id}/secrets/{secret_name}/versions/{secret_version}"


def secret_manager_sync(prefix: str, secret_name: str) -> SecretManagerSecretSource:
    return SecretManagerSecretSource(
        client=SecretManagerServiceClient(),
        project_id=require_env_var(prefix, secret_name, "PROJECT_ID"),
    )


__all__ = ["SecretManagerSource"]
