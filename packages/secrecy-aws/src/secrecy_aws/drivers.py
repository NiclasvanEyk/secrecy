import os

from secrecy.logging import logger

from secrecy_aws.sources.boto3.sync import SecretsManagerSecretSource


def boto3(prefix: str, name: str) -> SecretsManagerSecretSource:
    secret_id_var_name = f"{prefix}_SECRET_ID"
    secret_id = os.environ.get(secret_id_var_name)
    if secret_id is None:
        # TODO: Just use the name of the secret. Maybe we should also use
        #       a flag or something and pass that tot the secrets source. If
        #       the secret is not found, and the user did not explicitly define
        #       a secret_id, we could hint that they either need to create a
        #       matching secret in secrets manager, OR explicitly pass the name
        #       using this env var. That would be a good DX.
        logger.debug(
            f"{secret_id_var_name} environment variable not set. Using the secret name as the AWS secret id."
        )
        secret_id = name

    secret_id = secret_id.strip()
    if len(secret_id) == 0:
        raise Exception(f"{secret_id_var_name} is set, but empty")

    return SecretsManagerSecretSource(secret_id)
