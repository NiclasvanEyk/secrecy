import json
from typing import override

from boto3 import client as create_default_boto3_client
from secrecy.abc.sync import SecretsSource


class SecretsManagerSecretSource(SecretsSource):
    def __init__(
        self,
        secret_id: str,
        client=None,
    ) -> None:
        super().__init__()
        self._client = client or create_default_boto3_client("secretsmanager")
        self.secret_id = secret_id

    @override
    def pull(self) -> dict[str, str]:
        response = self._client.get_secret_value(SecretId=self.secret_id)
        serialized = response["SecretString"]
        return json.loads(serialized)

    @override
    def push(self, values: dict[str, str]) -> None:
        response = self._client.put_secret_value(
            SecretId=self.secret_id,
        )
        serialized = response["SecretString"]
        return json.loads(serialized)
