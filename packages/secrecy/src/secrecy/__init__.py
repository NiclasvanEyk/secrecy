"""The core interfaces and functionality of the `secrecy` ecosystem.

By itself, this package is useless, you need to pair it with one of the driver packages, that actually implement the details for how to retrieve images, e.g. from an encrypted file, your cloud provider, or your password manager.
"""

from secrecy._internals.core import JSON, Definition, WrapsDefinition
from secrecy._internals.source.registry import (
    MissingDefaultSourceError,
    SourceRegistry,
    UnknownSourceError,
    default_source,
    register_source,
)
from secrecy._internals.source.sync import Source
from secrecy._internals.sync import Secret, retrieve, validate

__all__ = [
    "Definition",
    "JSON",
    "MissingDefaultSourceError",
    "Secret",
    "Source",
    "SourceRegistry",
    "UnknownSourceError",
    "WrapsDefinition",
    "register_source",
    "default_source",
    "retrieve",
    "validate",
]
