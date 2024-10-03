from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class SecretsSource(Protocol):
    """
    A generic protocol for retreiving and storing a group of secrets.
    """

    @abstractmethod
    def pull(self) -> dict[str, str]:
        """
        Retreive the secrets from the source.
        """

    @abstractmethod
    def push(self, values: dict[str, str]) -> None:
        """
        Update the secrets in the source with the given ones.
        """
