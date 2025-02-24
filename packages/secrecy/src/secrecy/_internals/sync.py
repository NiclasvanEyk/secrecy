from typing import final, override

from secrecy._internals.core import Definition, WrapsDefinition, unwrap_definition
from secrecy._internals.dynamic import resolve_dynamic_source_factory
from secrecy._internals.source.registry import SourceRegistry, UnknownSourceError
from secrecy._internals.source.sync import Source
from secrecy.exception import SecrecyError


@final
class Secret[T = str](WrapsDefinition[T]):
    """A utility class for defining and accessing a secret.

    By default, this completely based on configuration through environment variables.
    """

    _definition: Definition[T]

    _source: Source

    def __init__(
        self,
        name: str,
        shape: type[T] = str,
        source: str | Source | None = None,
        source_registry: SourceRegistry | None = None,
    ) -> None:
        """Define a new secret.

        :param name: The unique name of your secret.
        :param shape: The data type of your secret. If you intend to e.g. store JSON in here, use :py:type:`secrecy.JSON`
        :param source: A shape
        :param source_registry: A shape
        """
        super().__init__()
        self._definition = Definition(name, shape)
        if isinstance(source, str):
            registry = source_registry or SourceRegistry.global_instance()
            resolved = registry.resolve(source)
            if not resolved:
                raise UnknownSourceError(f"Unknown source '{source}'")
            self._source = resolved
        else:
            self._source = source or DynamicSource()

    @override
    def definition(self) -> Definition[T]:
        return self._definition

    def validate(self) -> None:
        """Validate the configuration of the secret.

        This is just here for convenience.
        Read the docs of the `secrecy.validate` function for more information.
        """
        return validate(self, self._source)

    def retrieve(self) -> T:
        """Retrieve the secret value.

        This is just here for convenience.
        Read the docs of the `secrecy.retrieve` function for more information.
        """
        return retrieve(self, self._source)


@final
class DynamicSource(Source):
    """Dynamically constructs a source at runtime based on environment variables."""

    def _resolve[T](self, definition: Definition[T]) -> Source:
        factory, meta = resolve_dynamic_source_factory(definition.name)
        source = factory(definition.name)
        if not isinstance(source, Source):
            raise SecrecyError(
                f"Expected a 'secrecy.Source' object after running driver '{meta.driver}'. Got an instance of {type(source)}"
            )
        return source

    @override
    def validate[T](self, definition: Definition[T]) -> None:
        actual_source = self._resolve(definition)
        _ = actual_source.validate(definition)

    @override
    def fetch[T](self, definition: Definition[T]) -> T:
        actual_source = self._resolve(definition)
        return actual_source.fetch(definition)


def retrieve[T](secret: WrapsDefinition[T], source: Source | None = None) -> T:
    """Retrieve the secret value."""
    definition = unwrap_definition(secret)
    return (source or DynamicSource()).fetch(definition)


def validate[T](secret: WrapsDefinition[T], source: Source | None = None) -> None:
    """Validate the configuration of the secret.

    Note that for some secrets, this still does not guarantee, that the secret
    is properly configured. As an example, this method **can** validate, that
    you e.g. have specified proper credentials for fetching the secret from
    your cloud providers secret store. However, it can **not** guarantee that
    you did properly grant your application that proper access permission to
    the secret.
    """
    definition = unwrap_definition(secret)
    _ = (source or DynamicSource()).validate(definition)
