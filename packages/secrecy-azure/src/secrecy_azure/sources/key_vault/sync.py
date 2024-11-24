from typing import override

from secrecy.abc.sync import ReadableSecretsSource, WritableSecretsSource


class KeyVaultSecretSource(ReadableSecretsSource, WritableSecretsSource):
    def __init__(self) -> None:
        super().__init__()

    @override
    def pull(self) -> dict[str, str]:
        raise NotImplementedError()

    @override
    def push(self, values: dict[str, str]) -> None:
        raise NotImplementedError()
