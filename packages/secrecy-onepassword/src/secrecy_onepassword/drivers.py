import os

from onepassword import Client

from secrecy_onepassword.__about__ import __version__
from secrecy_onepassword.sources.sdk.asyncio import OnePasswordSdkSecretsSource


async def sdk(prefix: str, name: str) -> OnePasswordSdkSecretsSource:
    vault_id_env_var = f"{prefix}_VAULT_ID"
    vault_id = os.environ.get(vault_id_env_var)
    if vault_id is None:
        raise Exception(f"{vault_id_env_var} is required to be set!")

    item_id_env_var = f"{prefix}_ITEM_ID"
    item_id = os.environ.get(item_id_env_var)
    if item_id is None:
        raise Exception(f"{item_id_env_var} is required to be set!")

    well_known_env_token_env_var = "OP_SERVICE_ACCOUNT_TOKEN"
    service_account_token_env_var = f"{prefix}_{well_known_env_token_env_var}"
    service_account_token = os.environ.get(service_account_token_env_var)
    if service_account_token is None:
        service_account_token = os.environ.get(well_known_env_token_env_var)
        if service_account_token is None:
            raise Exception(
                f"Either {service_account_token_env_var} or {well_known_env_token_env_var} is required to be set!"
            )

    integration_name = os.environ.get(
        f"{prefix}_INTEGRATION_NAME", "secrecy_onepassword"
    )
    integration_version = os.environ.get(f"{prefix}_INTEGRATION_VERSION", __version__)

    client = await Client.authenticate(
        auth=service_account_token,
        integration_name=integration_name,
        integration_version=integration_version,
    )

    return OnePasswordSdkSecretsSource(
        client=client,
        vault_id=vault_id,
        item_id=item_id,
    )
