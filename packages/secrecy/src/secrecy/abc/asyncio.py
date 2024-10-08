from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class ReadableSecretsSource(Protocol):
    """
    A generic protocol for retreiving a group of secrets.
    """

    @abstractmethod
    async def pull(self) -> dict[str, str]:
        """
        Retreive the secrets from the source.
        """


@runtime_checkable
class WritableSecretsSource(Protocol):
    """
    A generic protocol for storing a group of secrets.
    """

    @abstractmethod
    async def push(self, values: dict[str, str]) -> None:
        """
        Update the secrets in the source with the given ones.
        """
