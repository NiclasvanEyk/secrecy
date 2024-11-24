import os
from abc import abstractmethod
from typing import Protocol, override, runtime_checkable

from secrecy.autoresolve.sync import resolve_source
from secrecy.typing import AnySource


@runtime_checkable
class SecretSourceFactory(Protocol):
    """A structured"""

    @abstractmethod
    def produces(self) -> str | type | None:
        """
        A short textual identifier of the source type produced by this factory.

        You can also return a type, or `None`, if there is dynamic logic involved,
        and the actual type cannot be known until building it.
        """

    @abstractmethod
    def __call__(self) -> AnySource:
        """Builds the actual source."""


class EnvironmentSecretSourceFactory(SecretSourceFactory):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    @override
    def produces(self) -> str | type | None:
        return os.environ.get(f"SECRECY_{self.name.casefold().upper()}_DRIVER")

    @override
    def __call__(self) -> AnySource:
        return resolve_source(self.name)
