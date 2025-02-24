from secrecy import Secret, Source


def infer_source_type(secret: Secret) -> Source | None:
    # TODO
    # if callable(source):
    #     if isinstance(source, Source):
    #         return source.produces()

    #     signature = get_signature(source)
    #     return_type = signature.return_annotation
    #     if isinstance(return_type, ReadableSecretsSource):
    #         return return_type
    # else:
    #     print(f"{source} is not callable")

    return None
