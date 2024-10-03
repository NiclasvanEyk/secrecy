import os

import pytest
from secrecy.autoresolve.sync import secrecy


async def test_it_works():
    os.environ["SECRECY_FOO_DRIVER"] = "aws-boto3"
    os.environ["AWS_ACCESS_KEY_ID"] = require("SECRECY_TESTS_AWS_ACCESS_KEY_ID")
    os.environ["AWS_SECRET_ACCESS_KEY"] = require("SECRECY_TESTS_AWS_SECRET_ACCESS_KEY")
    os.environ["AWS_DEFAULT_REGION"] = require("SECRECY_TESTS_AWS_DEFAULT_REGION")
    os.environ["SECRECY_FOO_SECRET_ID"] = require("SECRECY_TESTS_AWS_SECRET_ID")

    secrets = secrecy("foo")
    assert secrets == {
        "user": "some-user",
        "password": "the-password",
    }


def require(env_var_name: str) -> str:
    value = os.environ.get(env_var_name)
    if value is None:
        pytest.skip(f"{env_var_name} not present, skipping aws integration tests...")
    return value
