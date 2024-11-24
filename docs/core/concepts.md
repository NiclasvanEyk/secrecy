# Concepts

A "secret" can mean many things.
This page clarifies important concepts and defines words in the context of Secrecy.

## Configuration

As mentioned in the [introduction](../index.md), your source code can look the same regardless where you store your secrets.
However, something needs to tell Secrecy where your secrets are stored, and potentially how to authenticate with that storage.
This is done via _environment variables_.

In general, your secrets always have a _name_.
This name uniquely identifies them in the context of your application.
The [introduction](../index.md) used `database_credentials` as the name:

```python hl_lines="4"
from secrecy import fetch_secret
from my_app.database import connect_to_db

db_secrets = fetch_secret(name="database_credentials")
db_connection = connect_to_db(url=db_secrets["url"])
```

To now tell Secrecy how to fetch our `database_credentials` secret, we use [_environment variables_](https://en.wikipedia.org/wiki/Environment_variable).
There are numerous ways of defining them, so this document does not go into detail and instead uses the Unix conventions of `VARIABLE_NAME=value` for denoting their existence.

To now configure the retrieval of our `database_credentials` secret, we need to set the right variables.
All variables for a specific secret are prefixed by `SECRECY_` and their uppercase name.
This is also why the names should generally be in snake_case.

The environment variables for our `database_credentials` secret will therefore all start with `SECRECY_DATABASE_CREDENTIALS`.
There is only one required variable (you will learn why in a minute), which is the _driver_.
Again, we prepend our prefix, and use the uppercase of "driver", so one example would be

```bash
SECRECY_DATABASE_CREDENTIALS_DRIVER=encrypted_file
```

## Drivers

The _driver_ determines the _storage backend_ for the secret.
It defines whether to use [1Password](../ecosystem/password_managers/onepassword.md),
[an encrypted file](../ecosystem/simple_solutions/encrypted_files.md),
or your [Azure Key Vault](../ecosystem/cloud_providers/azure.md).

TODO: Say that driver is the python glue code by secrecy, and the storage backend is the actual service storing your secrets, e.g. 1Password.

Different drivers also require different environment variables to be set.
You can check the docs of each driver to learn which ones are supported.
For example, when using the [AWS Secrets Manager](../ecosystem/cloud_providers/aws.md) driver you can use the following values to explicitly pass credentials to the driver:

```bash
SECRECY_SECRETNAME_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
SECRECY_SECRETNAME_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

However, in the AWS ecosystem it is a common convention to read these credentials from conventionally known environment variables:

```bash
AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

Both options work perfectly fine.

## Types of Secrets

Some platforms, like the aforementioned [AWS Secrets Manager](https://aws.amazon.com/secrets-manager) store a bundle of key-value pairs as a secret.
Others, such as the [Google Cloud Secret Manager](https://cloud.google.com/security/products/secret-manager) only associate a single value with a secret.

### Single-Valued Secrets

Many storage backends

```python
from secrecy import fetch_secret

fetch_secret("db_password")
# => "7zWLG4xQzfLGX6"
```

### Secret Bundles

```python
from secrecy import fetch_secret_bundle

fetch_secret_bundle("db_connection")
# => {
#  "user": "app",
#  "password": "7zWLG4xQzfLGX6",
#  "host": "..."
# }
```

### Choosing
