from typing import TYPE_CHECKING, Any, override

from boto3 import client as create_default_boto3_client
from secrecy import Definition, Source
from secrecy.serialization import serialize_from_string

if TYPE_CHECKING:
    try:
        from mypy_boto3_secretsmanager import SecretsManagerClient
    except ImportError:
        type SecretsManagerClient = Any
else:
    type SecretsManagerClient = Any


class SecretsManagerSource(Source):
    _client: SecretsManagerClient

    def __init__(self, client: SecretsManagerClient = None) -> None:
        super().__init__()
        self._client = client or create_default_boto3_client("secretsmanager")

    @override
    def fetch[T](self, definition: Definition[T]) -> T:
        response = self._client.get_secret_value(SecretId=definition.name)
        return serialize_from_string(definition, response["SecretString"])

    @override
    def validate[T](self, definition: Definition[T]) -> None:
        # TODO:
        self._client.describe_secret()
