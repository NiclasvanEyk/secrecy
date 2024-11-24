"""Caching already retrieved secret values or resolved sources."""

from asyncio import iscoroutinefunction, run
from collections.abc import Callable

from secrecy.typing import AnySource, PendingSource


class CachedSecretValues:
    def __init__(
        self,
        values: dict[str, str],
    ):
        self._original_values = values
        self._values = values

    @property
    def has_pending_changes(self) -> bool:
        return set(self._original_values.items()) == set(self._values.items())

    def as_dict(self) -> dict[str, str]:
        return dict(self._values)

    def __getitem__(self, attr: str) -> str:
        return self._values[attr]

    def __setitem__(self, attr: str, value: str) -> None:
        self._values[attr] = value


class LazySourceCache:
    """Caches an instance of a secret source"""

    _cached_source: None | AnySource

    def __init__(self, source: PendingSource) -> None:
        self._pending_source = source
        self._cached_source = None

    def lazy_get(self) -> AnySource:
        """Lazily builds the source if necessary"""
        if self._cached_source is not None:
            return self._cached_source

        if isinstance(self._pending_source, AnySource):
            self._cached_source = self._pending_source
            return self._pending_source

        self._cached_source = self._pending_source()
        return self._cached_source


class LazySecretCache:
    _cached_values: None | CachedSecretValues

    def __init__(self, source: Callable[[], AnySource]) -> None:
        self._source = source
        self._cached_values = None

    def lazy_get(self) -> CachedSecretValues:
        """Lazily builds the source if necessary"""
        if self._cached_values is not None:
            return self._cached_values

        source = self._source()
        if iscoroutinefunction(source.pull):
            values = run(source.pull)
        else:
            values = source.pull()
        self._cached_values = CachedSecretValues(values)
        return self._cached_values
