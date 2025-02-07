from secrecy.abc.sync import WritableSecretsSource


def test_source(source: WritableSecretsSource) -> None:
    values = {"password": "s3cr3t"}

    source.push(values)
    assert source.pull() == values
