from secrecy.autoresolve.asyncio import resolve_source as resolve_source_async
from secrecy.autoresolve.sync import resolve_source
from secrecy.typing import AnyAsyncSource, AnySyncSource


class Environment:
    @staticmethod
    def secret(name: str) -> AnySyncSource:
        return resolve_source(name)

    @staticmethod
    async def async_secret(name: str) -> AnyAsyncSource:
        return await resolve_source_async(name)
