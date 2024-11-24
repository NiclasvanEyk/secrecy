"""
The simple environment-variable-based API, which most peoples will use to
simplify their secret retrieval.
"""

from secrecy.abc.asyncio import ReadableSecretsSource
from secrecy.exception import SecrecyError
from secrecy.internals import resolve_source_factory


async def resolve_source(name: str) -> ReadableSecretsSource:
    source_factory, meta = resolve_source_factory(name)
    source = await source_factory(meta.prefix, meta.name)
    if not isinstance(source, ReadableSecretsSource):
        raise SecrecyError(
            f"Expected a valid SecretsSource object after calling {meta.driver_module_specifier}. Got: {source}"
        )
    return source


async def secrecy(name: str) -> dict[str, str]:
    """
    Retrieves secrets based on the presence of environment variables.
    """
    source = await resolve_source(name)

    return await source.pull()
