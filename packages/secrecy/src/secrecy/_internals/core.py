from abc import abstractmethod
from collections.abc import Mapping
from typing import Protocol, final, runtime_checkable

type JSON = None | str | int | float | bool | Mapping[str, JSON]


@final
class Definition[T = str]:
    """Defines a secret together with an optional description of its shape."""

    name: str
    """
    The unique name of a secret.

    Unique here refers to the context of **your** application / use-case.
    """

    data_type: type[T]
    """
    The data type or shape of your secret.

    Note that this needs to be serializable to JSON to support multiple
    different storage backends. This way, you can e.g. store related
    configuration values in a single secret, but also in a structured way.

    Think of database credentials. You could store a single connection string
    such as `postgres://joe:p455w0rd@localhost:1234/my-database`. This is a
    wide-spread format and supported by many database. You could also store all
    of these in JSON, e.g.:

    ```json
    {
        "driver": "postgres",
        "user": "user",
        "password": "p455w0rd",
        "host": "localhost",
        "port": 1234,
        "database": "my-database"
    }
    ```

    One could argue, that the only "secret" value here is the password, but
    some related fields, such as `host` or `port` might also differ between
    environments.
    """

    def __init__(self, name: str, data_type: type[T] = str) -> None:
        """Construct a new secret defintion.

        Check the class- and property-level documentation for more detailed
        information.
        """
        super().__init__()
        self.name = name
        self.data_type = data_type


@runtime_checkable
class WrapsDefinition[T](Protocol):
    """An object that can be used in place of a definition.

    Mostly intended for the generic `Secret` utility class, that wraps a
    definition and places lots of useful methods on it (eases discovery).
    """

    @abstractmethod
    def definition(self) -> Definition[T]:
        """Return the wrapped secret definition."""
        pass


def unwrap_definition[T](secret: WrapsDefinition[T] | Definition[T]) -> Definition[T]:
    if isinstance(secret, Definition):
        return secret

    if isinstance(secret, WrapsDefinition):
        return unwrap_definition(secret.definition())

    raise TypeError(f"Could not unwrap secret definition for {secret}")
