"""
Pulls all values from the environment, if they have the common prefix.

If I e.g. have the secret name FOO, and the following env vars:

```dotenv
SECRECY_FOO_DRIVER="environment"
SECRECY_FOO_API_KEY="123-abc-xyz"
SECRECY_FOO_USER="the-next-facebook"
```

It would lead to the following secrets being retrieved

```json
{
    "api_key": "123-abc-xyz",
    "user": "the-next-facebook"
}
```
"""
