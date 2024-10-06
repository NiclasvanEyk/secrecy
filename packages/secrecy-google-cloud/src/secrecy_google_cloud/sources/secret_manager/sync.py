import json
from typing import override

from google.cloud.secretmanager import SecretManagerServiceClient
from secrecy.abc.sync import SecretsSource


class SecretManagerSecretSource(SecretsSource):
    def __init__(
        self,
        client: SecretManagerServiceClient,
        project_id: str,
        secret_name: str,
        secret_version: str,
    ) -> None:
        super().__init__()
        self.client = client
        self.project_id = project_id
        self.secret_name = secret_name
        self.secret_version = secret_version

    @override
    def pull(self) -> dict[str, str]:
        response = self.client.access_secret_version(name=self.resource_name())
        payload = response.payload.data.decode("UTF-8")
        return json.loads(payload)

    def resource_name(self) -> str:
        return f"projects/{self.project_id}/secrets/{self.secret_name}/versions/{self.secret_version}"

    @override
    def push(self, values: dict[str, str]) -> None:
        raise NotImplementedError
