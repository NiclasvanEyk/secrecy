"""Common type definitions."""
from collections.abc import Callable

from secrecy.abc.asyncio import ReadableSecretsSource as AsyncReadableSecretsSource
from secrecy.abc.asyncio import WritableSecretsSource as AsyncWritableSecretsSource
from secrecy.abc.sync import ReadableSecretsSource, WritableSecretsSource

AnySyncSource = ReadableSecretsSource | WritableSecretsSource
AnyAsyncSource = AsyncReadableSecretsSource | AsyncWritableSecretsSource
AnySource = AnySyncSource | AnyAsyncSource
"""Union of all possible sources, sync or async."""

PendingSource = AnySource | Callable[[], AnySource]
"""Something that may become a source"""
