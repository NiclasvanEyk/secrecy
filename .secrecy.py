from abc import abstractmethod
from collections.abc import Callable
from typing import Protocol, runtime_checkable

from secrecy.abc.asyncio import ReadableSecretsSource as AsyncReadableSecretsSource
from secrecy.abc.asyncio import WritableSecretsSource as AsyncWritableSecretsSource
from secrecy.abc.sync import ReadableSecretsSource, WritableSecretsSource
from secrecy.autoresolve.asyncio import resolve_source as resolve_secret_from_env_async
from secrecy.autoresolve.sync import resolve_source as resolve_secret_from_env

AnySyncSource = ReadableSecretsSource | WritableSecretsSource
AnyAsyncSource = AsyncReadableSecretsSource | AsyncWritableSecretsSource


@runtime_checkable
class Driver[Source: AnySyncSource](Protocol):
    @abstractmethod
    def build_source() -> Source:
        pass


@runtime_checkable
class AsyncDriver[Source: AnyAsyncSource](Protocol):
    @abstractmethod
    async def build_source() -> Source:
        pass


class SecretDefinition[Source: AnySyncSource]:
    name: str

    def __init__(self, name: str, source: Source | Callable[[], Source]) -> None:
        self.name = name
        self._source = source

    @classmethod
    def env(cls, name: str, lazy: bool = False) -> "SecretDefinition[Source]":
        def resolver() -> Callable[[], SecretDefinition[Source]]:
            return resolve_secret_from_env(name)

        return SecretDefinition[Source](
            name=name, source=resolver if lazy else resolver()
        )


class AsyncSecretDefinition[Source: AnyAsyncSource]:
    name: str

    def __init__(self, name: str, source: Source | Callable[[], Source]) -> None:
        self.name = name
        self._source = source

    @classmethod
    async def env(cls, name: str, lazy: bool = False) -> "SecretDefinition[Source]":
        async def resolver() -> Callable[[], SecretDefinition[Source]]:
            source = await resolve_secret_from_env_async(name)
            return source

        source = resolver
        if lazy:
            source = await resolver()
        return SecretDefinition[Source](name=name, source=source)


# ----------------------------------------------------------------

db_secret = Secret("db_credentials")
db_connection = db_secret.fetch()
db_password = db_connection["password"]

definition = SecretDefinition("database_credentials", FileDriver())
definition = SecretDefinition.env("database_credentials")
credentials = definition.fetch()
