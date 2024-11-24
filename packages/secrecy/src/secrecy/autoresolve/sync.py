"""
The simple environment-variable-based API, which most peoples will use to
simplify their secret retrieval.
"""

from secrecy.abc.sync import ReadableSecretsSource
from secrecy.exception import SecrecyError
from secrecy.internals import resolve_source_factory


def resolve_source(name: str) -> ReadableSecretsSource:
    source_factory, meta = resolve_source_factory(name)
    source = source_factory(meta.prefix, meta.name)
    if not isinstance(source, ReadableSecretsSource):
        raise SecrecyError(
            f"Expected a valid SecretsSource object after calling {meta.driver_module_specifier}. Got: {source}"
        )
    return source


def secrecy(name: str) -> dict[str, str]:
    """
    Retrieves secrets based on the presence of environment variables.
    """

    return resolve_source(name).pull()
