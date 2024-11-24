from pathlib import Path

from secrecy_file.sources.encrypted_file.sync import EncryptedFileSecretsSource


def encrypted_file(prefix: str, secret_name: str) -> EncryptedFileSecretsSource:
    path = optional_environment_variable(
        prefix, "FILES_PATH", str(Path.cwd() / "secrets")
    )
    path = Path(path)

    encryption_key = require_environment_variable(prefix, secret_name, "ENCRYPTION_KEY")

    return EncryptedFileSecretsSource(path=path, key=encryption_key.encode("utf-8"))
