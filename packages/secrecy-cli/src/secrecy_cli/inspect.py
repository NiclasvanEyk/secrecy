from inspect import signature as get_signature

from secrecy.abc.sync import ReadableSecretsSource
from secrecy.secret import Secret
from secrecy.source import SecretSourceFactory


def infer_source_type(secret: Secret) -> ReadableSecretsSource | None:
    source = secret._source._pending_source

    if callable(source):
        if isinstance(source, SecretSourceFactory):
            return source.produces()

        signature = get_signature(source)
        return_type = signature.return_annotation
        if isinstance(return_type, ReadableSecretsSource):
            return return_type
    else:
        print(f"{source} is not callable")

    return None
