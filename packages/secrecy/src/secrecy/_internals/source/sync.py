from abc import ABC, abstractmethod

from secrecy._internals.core import Definition


class Source(ABC):
    """Wraps all state and configuration needed to retrieve the value of a secret."""

    @abstractmethod
    def fetch[T](self, definition: Definition[T]) -> T:
        """Retrieve the value of a secret."""

    @abstractmethod
    def validate[T](self, definition: Definition[T]) -> None:
        """Validate that everything is configured, so that we can fetch the definition at runtime.

        The rule of thumb is, that
        """
        # TODO: Continue documentation
