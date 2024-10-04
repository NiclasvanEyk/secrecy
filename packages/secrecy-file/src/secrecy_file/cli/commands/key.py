"""
generate a new encryption key
"""

from argparse import ArgumentParser

from secrecy_file.sources.encrypted_file.sync import EncryptedFileSecretsSource


def configure(command: ArgumentParser) -> None:
    pass


def execute() -> None:
    print(EncryptedFileSecretsSource.generate_key().decode("utf-8"))
