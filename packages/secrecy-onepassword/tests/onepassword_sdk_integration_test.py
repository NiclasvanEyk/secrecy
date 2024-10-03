import os

import pytest
from secrecy.autoresolve.asyncio import secrecy

TEST_VAULT_ENV_VAR = "SECRECY_TESTS_1PW_VAULT_ID"
TEST_ITEM_ENV_VAR = "SECRECY_TESTS_1PW_ITEM_ID"
TEST_SERVICE_ACCOUNT_ENV_VAR = "SECRECY_TESTS_1PW_SERVICE_ACCOUNT_TOKEN"


@pytest.mark.asyncio
async def test_it_works():
    vault_id = os.environ.get(TEST_VAULT_ENV_VAR)
    if vault_id is None:
        pytest.skip(
            f"{TEST_VAULT_ENV_VAR} not present, skipping 1pw integration tests..."
        )
        return

    item_id = os.environ.get(TEST_ITEM_ENV_VAR)
    if item_id is None:
        pytest.skip(
            f"{TEST_ITEM_ENV_VAR} not present, skipping 1pw integration tests..."
        )
        return

    service_account_token = os.environ.get(TEST_SERVICE_ACCOUNT_ENV_VAR)
    if service_account_token is None:
        pytest.skip(
            f"{TEST_SERVICE_ACCOUNT_ENV_VAR} not present, skipping 1pw integration tests..."
        )
        return

    os.environ["SECRECY_FOO_DRIVER"] = "onepassword-sdk"
    os.environ["SECRECY_FOO_VAULT_ID"] = vault_id
    os.environ["SECRECY_FOO_ITEM_ID"] = item_id
    os.environ["SECRECY_FOO_OP_SERVICE_ACCOUNT_TOKEN"] = service_account_token

    secrets = await secrecy("foo")
    assert secrets == {
        "user": "some-user",
        "password": "the-password",
    }
