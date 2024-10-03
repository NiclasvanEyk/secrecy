from abc import abstractmethod
from typing import Protocol, override

from cryptography.fernet import Fernet


class SymmetricEncryption(Protocol):
    @abstractmethod
    def encrypt(self, value: bytes, key: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, value: bytes, key: bytes) -> bytes:
        pass


class FernetEncryption(SymmetricEncryption):
    @override
    def encrypt(self, value: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(value)

    @override
    def decrypt(self, value: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(value)
