from typing import override

from google.cloud.secretmanager import SecretManagerServiceClient
from secrecy import Definition, Source
from secrecy.serialization import serialize_from_string


class SecretManagerSecretSource(Source):
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
