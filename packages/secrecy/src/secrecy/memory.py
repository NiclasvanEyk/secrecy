from typing import override

from secrecy.abc.sync import SecretsSource


class InMemorySecretsSource(SecretsSource):
    """
    Stores secrets in a dictionary in memory.

    This is not safe, and is intended for testing purposes only!
    """

    def __init__(self, values: dict[str, str]) -> None:
        super().__init__()
        self.values = values

    @override
    def pull(self) -> dict[str, str]:
        return self.values

    @override
    def push(self, values: dict[str, str]) -> None:
        self.values = values
