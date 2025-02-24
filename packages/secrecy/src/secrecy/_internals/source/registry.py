from __future__ import annotations

import os
from collections import OrderedDict
from collections.abc import Callable
from typing import ClassVar, overload

from secrecy._internals.source.sync import Source

type AnySource = Source

type _SourceFactory = Callable[[], AnySource]
type _DecoratedFactory = Callable[[_SourceFactory], None]


class MissingDefaultSourceError(Exception):
    """Raised when attempting to resolve the default source, but none was specified."""


class UnknownSourceError(Exception):
    """Raised when attempting to resolve a source by name, but no source was previously registered with said name."""


class SourceRegistry:
    default_source: str | None
    """The source that will be used by default if a secret does not specify one explicitly."""

    _factories: dict[str, Callable[[], AnySource]]

    _implicit_factories: dict[str, type[AnySource]]

    _global: ClassVar[SourceRegistry | None] = None

    def __init__(self, default_source: str | None = None) -> None:
        self._factories = dict()
        self._implicit_factories = dict()
        self.default_source = default_source

    @classmethod
    def global_instance(cls) -> SourceRegistry:
        if cls._global is None:
            registry = SourceRegistry()
            cls._global = registry
            return registry
        else:
            return cls._global

    @staticmethod
    def from_environment() -> SourceRegistry:
        registry = SourceRegistry()

        relevant_vars = OrderedDict(
            {
                k.removeprefix("SECRECY_SOURCE_"): v
                for k, v in os.environ.items()
                if k.startswith("SECRECY_SOURCE_")
            }
        )

        current_source = None
        for key, value in relevant_vars:
            pass

        return registry

    @overload
    def add(self, name: str, *, default: bool = False) -> _DecoratedFactory: ...

    @overload
    def add(
        self,
        name: str,
        factory: type[AnySource] | Callable[[], AnySource],
        default: bool = False,
    ) -> None: ...

    def add(
        self,
        name: str,
        factory: type[AnySource] | Callable[[], AnySource] | None = None,
        default: bool = False,
    ) -> _SourceFactory | _DecoratedFactory | None:
        if default:
            self.default_source = name

        if isinstance(factory, type):
            self._implicit_factories[name] = factory
            return None

        # Explicitly register a passed function or lambda for the given name
        if callable(factory):
            self._factories[name] = factory
            return None

        # Register the decorated function for the given name
        def decorator(source: Callable[[], AnySource]):
            self._factories[name] = source

        return decorator

    def resolve(self, name: str | None = None) -> AnySource | None:
        name = name or self.default_source
        if name is None:
            raise MissingDefaultSourceError(
                "You did not specify a source name, and no default source was specified"
            )

        factory = self._factories.get(name, None)
        if factory:
            return factory()

        target_type = self._implicit_factories.get(name, None)
        if target_type:
            # try autoconfig
            raise RuntimeError("Still needs to be implemented")


@overload
def register_source(name: str, *, default: bool = False) -> _DecoratedFactory: ...


@overload
def register_source(
    name: str, factory: type[AnySource] | Callable[[], AnySource], default: bool = False
) -> None: ...


def register_source(
    name: str,
    factory: type[AnySource] | Callable[[], AnySource] | None = None,
    default: bool = False,
) -> _SourceFactory | _DecoratedFactory | None:
    return SourceRegistry.global_instance().add(name, factory, default)


@overload
def default_source() -> str | None: ...


@overload
def default_source(name: str) -> None: ...


def default_source(name: str | None = None) -> str | None:
    """Set or return the name of the global default source."""
    registry = SourceRegistry.global_instance()

    if name is None:
        return registry.default_source

    registry.default_source = name
