from secrecy_file.sources.encrypted_file.sync import EncryptedFileSecretsSource


def main() -> None:
    print(EncryptedFileSecretsSource.generate_key().decode("utf-8"))
