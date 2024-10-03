# Secrecy for 1Password

## Getting Started

Install the package:

```shell
pip install secrecy-onepassword
```

Assuming you want to fetch a secret named `MY_SECRET`, setup the following environment variables.

This one sets the driver to this package

```dotenv
SECRECY_MY_SECRET_DRIVER="onepassword-sdk"
```

These two identify the item that is used to fetch secrets from.

> [!NOTE]
> You can find the ids by [...]

```dotenv
SECRECY_MY_SECRET_VAULT_ID=""
SECRECY_MY_SECRET_ITEM_ID=""
```

Then you need to setup authentication. You can either set a global

```dotenv
OP_SERVICE_ACCOUNT_TOKEN=""
```

or use one for a specific secret:

```dotenv
SECRECY_MY_SECRET_OP_SERVICE_ACCOUNT_TOKEN=""
```

