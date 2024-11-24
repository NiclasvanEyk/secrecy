import os

from secrecy_aws.sources.boto3.sync import SecretsManagerSecretSource


def boto3(prefix: str, name: str) -> SecretsManagerSecretSource:
    secret_id_var_name = f"{prefix}_SECRET_ID"
    secret_id = os.environ.get(secret_id_var_name)
    if secret_id is None:
        raise Exception(
            f"{secret_id_var_name} is required to be set as an environment variable"
        )

    secret_id = secret_id.strip()
    if len(secret_id) == 0:
        raise Exception(f"{secret_id_var_name} is set, but empty")

    # TODO: Support passing configuration options to the client explicitly for this secret.
    #       This would unlock loading secrets from different regions, accounts, etc.

    return SecretsManagerSecretSource(secret_id)
