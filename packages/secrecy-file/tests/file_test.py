from pathlib import Path

from secrecy_file.sources.encrypted_file.sync import EncryptedFileSecretsSource


def test_can_encrypt_and_decrypt_files(tmp_path: Path) -> None:
    tmp_file = tmp_path / "secrets.encrypted"
    key = EncryptedFileSecretsSource.generate_key()

    source = EncryptedFileSecretsSource(tmp_file, key=key)
    source.push({"api_key": "abc-1234"})

    with tmp_file.open() as file:
        contents = file.read()
        assert "api_key" not in contents, "It seems like the file is in plaintext"

    values = source.pull()
    assert values == {"api_key": "abc-1234"}
