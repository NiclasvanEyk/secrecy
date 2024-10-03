from json import dumps, loads
from pathlib import Path
from typing import override

from cryptography.fernet import Fernet
from secrecy.abc.sync import SecretsSource

from secrecy_file.encryption import FernetEncryption, SymmetricEncryption


class EncryptedFileSecretsSource(SecretsSource):
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
