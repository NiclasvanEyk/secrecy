import os

import pytest
from secrecy.autoresolve.sync import secrecy

SECRET_ID_VAR_NAME = "SECRECY_TESTS_AWS_SECRET_ID"


@pytest.mark.asyncio
async def test_it_works():
    for var in (
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_DEFAULT_REGION",
    ):
        if os.environ.get(var) is None:
            pytest.skip(f"{var} not present, skipping aws integration tests...")

    secret_id = os.environ.get(SECRET_ID_VAR_NAME)
    if secret_id is None:
        pytest.skip(
            f"{SECRET_ID_VAR_NAME} not present, skipping aws integration tests..."
        )

    os.environ["SECRECY_FOO_DRIVER"] = "aws-boto3"
    os.environ["SECRECY_FOO_SECRET_ID"] = secret_id

    secrets = secrecy("foo")
    assert secrets == {
        "user": "some-user",
        "password": "the-password",
    }
