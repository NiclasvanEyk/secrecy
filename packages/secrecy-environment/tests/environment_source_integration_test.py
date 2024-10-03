import os

from secrecy.autoresolve.sync import secrecy


def test_it_works_with_autoconfiguration() -> None:
    # This is the example from the module doc

    os.environ["SECRECY_FOO_DRIVER"] = "environment"
    os.environ["SECRECY_FOO_API_KEY"] = "123-abc-xyz"
    os.environ["SECRECY_FOO_USER"] = "the-next-facebook"

    secrets = secrecy("foo")
    assert set(secrets.items()).issuperset(
        {
            ("api_key", "123-abc-xyz"),
            ("user", "the-next-facebook"),
        }
    )
