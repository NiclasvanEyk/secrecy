from collections.abc import Callable
from json import dumps, loads
from pathlib import Path
from typing import override

from cryptography.fernet import Fernet
from secrecy.abc.sync import ReadableSecretsSource, WritableSecretsSource
from secrecy.autoresolve.environment import require_environment_variable
from secrecy.exception import SecrecyError
from secrecy.secret import Secret
from secrecy.source import SecretSourceFactory
from secrecy.typing import AnySource

from secrecy_file.encryption import FernetEncryption, SymmetricEncryption


class EncryptedFileSecretsSource(ReadableSecretsSource, WritableSecretsSource):
    """
    A collection of secret values stored in an encrypted file on the filesystem.
    """

    path: Path
    """
    The path where the encrypted file should be stored.
    """

    def __init__(
        self,
        path: str | Path,
        key: bytes,
        encryption: SymmetricEncryption | None = None,
    ) -> None:
        super().__init__()
        self.path = Path(path)
        self._key = key
        self._encryption = encryption or FernetEncryption()

    @classmethod
    def generate_key(cls) -> bytes:
        # For convenience. This way you don't need to import another class.
        return Fernet.generate_key()

    @override
    def pull(self) -> dict[str, str]:
        with self.path.open("rb") as file:
            encrypted = file.read()
            decrypted = self._encryption.decrypt(encrypted, self._key)
            return loads(decrypted.decode("utf-8"))  # type: ignore

    @override
    def push(self, values: dict[str, str]) -> None:
        decrypted = dumps(values).encode("utf-8")
        encrypted = self._encryption.encrypt(decrypted, self._key)
        with self.path.open("wb") as file:
            _ = file.write(encrypted)


class FileSecretSourceFactory(SecretSourceFactory):
    def __init__(
        self, name: str, callable: Callable[[], EncryptedFileSecretsSource]
    ) -> None:
        super().__init__()
        self.name = name
        self.callable = callable

    @override
    def produces(self) -> type | None:
        return EncryptedFileSecretsSource

    @override
    def __call__(self) -> AnySource:
        return self.callable()


class EncryptedFiles:
    def __init__(self, directory: Path | str, key: bytes | None = None) -> None:
        self.directory = Path(directory)
        self.key = key

    @staticmethod
    def from_env(name: str) -> "EncryptedFiles":
        file_path = Path(require_environment_variable(f"SECRECY_{name}", name, "PATH"))
        key_path = Path(require_environment_variable(f"SECRECY_{name}", name, "KEY"))
        with Path(key_path).open("rb") as file:
            return EncryptedFiles(directory=file_path, key=file.read())

    def secret(self, name: str, key: bytes | None = None) -> Secret:
        def builder():
            final_key = key if key is not None else self.key
            if final_key:
                raise SecrecyError("A key needs to be specified!")

            final_path = self.directory / name
            if not final_path.exists():
                raise SecrecyError(f"File '{final_path}' does not exist!")

            return EncryptedFileSecretsSource(final_path, final_key)

        return Secret(name, source=FileSecretSourceFactory(name, builder))
