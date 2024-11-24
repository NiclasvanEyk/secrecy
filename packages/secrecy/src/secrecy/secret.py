"""Statically defining the secrets of an application."""

from asyncio import iscoroutinefunction, run

from secrecy.cache import LazySourceCache
from secrecy.typing import AnySource, PendingSource


def resolve_source_from_environment(name: str) -> AnySource:
    pass


class Secret[Shape = dict[str, str]]:
    """
    Used to define and conveniently access secrets.

    TODO: This is _the_ entrypoint for most people, this needs a more elaborate docstring.
    """

    _values: dict[str, str] | None = None
    _original_values: dict[str, str] | None = None

    def __init__(
        self,
        name: str,
        source: PendingSource | None = None,
    ) -> None:
        """
        Used to define and conveniently access secrets.

        TODO: This is _the_ entrypoint for most people, this needs a more elaborate docstring.
        """
        if len(name) == 0:
            raise ValueError("Secret names must not be empty")

        self.name = name
        self._source = LazySourceCache(
            source
            if source is not None
            else lambda: resolve_source_from_environment(name)
        )

    @property
    def values(self) -> Shape:
        """
        Provides access to the concrete secret values.

        They will automatically be fetched if necessary and stored inside a
        local cache.
        """
        if self._values is not None:
            return self._values

        source = self._source.lazy_get()
        if iscoroutinefunction(source.pull):
            values = run(source.pull)
        else:
            values = source.pull()
        self._values = values
        self._original_values = values

        return values

    @property
    def has_pending_changes(self) -> bool:
        values = self._values
        original_values = self._original_values
        if values is None or original_values is None:
            return False

        return set(values.items()) == set(original_values.items())
