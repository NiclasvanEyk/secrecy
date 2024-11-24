from json import loads
from pathlib import Path
from typing import override

from secrecy.abc.sync import ReadableSecretsSource


class DockerSecretsSource(ReadableSecretsSource):
    def __init__(self, secret_name: str, secrets_directory: Path) -> None:
        super().__init__()
        self.secret_name = secret_name
        self.secrets_directory = secrets_directory

    @override
    def pull(self) -> dict[str, str]:
        secrets_file_path = self.secrets_directory / self.secret_name
        with secrets_file_path.open() as secrets_file:
            return loads(secrets_file.read())
