import os
from typing import override

from secrecy import Definition, Source

INTERNAL_KEYS = {
    "driver",
}


class EnvironmentVariablesSecretsSource[T](Source):
    @override
    def fetch(self, definition: Definition[T]) -> T:
        """Retrieve the value of a secret."""

    @override
    def validate(self, definition: Definition[T]) -> T:
        secrets: dict[str, str] = {}
        for prefixed_key, value in os.environ.items():
            if prefixed_key.startswith(self.prefix):
                key = prefixed_key.removeprefix(self.prefix).removeprefix("_")
                key = key.lower()

                # Don't add e.g. the driver to the secrets
                if key in INTERNAL_KEYS:
                    continue

                secrets[key] = value
        return secrets
