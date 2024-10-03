import logging
import os
from typing import override

from secrecy.abc.sync import SecretsSource

INTERNAL_KEYS = {
    "driver",
}


class EnvironmentVariablesSecretsSource(SecretsSource):
    def __init__(self, prefix: str) -> None:
        super().__init__()
        self.prefix = prefix

    @override
    def pull(self) -> dict[str, str]:
        secrets: dict[str, str] = {}
        for key, value in os.environ.items():
            if key.startswith(self.prefix):
                sanitized_key = key.removeprefix(self.prefix).removeprefix("_")
                sanitized_key = sanitized_key.lower()

                # Don't add e.g. the driver to the secrets
                if sanitized_key in INTERNAL_KEYS:
                    continue

                secrets[sanitized_key] = value
        return secrets

    @override
    def push(self, values: dict[str, str]) -> None:
        logging.warning(
            "It does not make sense to change secrets when using the environment-variable driver! This has no effect."
        )
