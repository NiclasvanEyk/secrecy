# Secrecy for Environment Variables

This is

## Getting Started

Install the package from PyPi

```shell
pip install secrecy-environment
```

> [!IMPORTANT]
> The following guide assumes that you define a secret named `my_secret`.
> Read more about [secret names in the documentation](https://github.com/NiclasvanEyk/secrecy#secret-names)

Set the driver by defining the following environmen variable

```dotenv
SECRECY_MY_SECRET_DRIVER="environment"
```

Then define environment variables with a prefix.

```dotenv
SECRECY_MY_SECRET_USERNAME="my-username"
SECRECY_MY_SECRET_PASSWORD="my-password"
SECRECY_MY_SECRET_WHATEVER="whatever else you want to store"
```

Then in the Python file you want to use

<!-- SECRECY_USAGE_EXAMPLE -->
```python
from secrecy.autoresolve.sync import secrecy

secret = secrecy("my_secret")
# {
#    "username": "my-username",
#    "password": "my-password",
#    "whatever": "whatever else you want to store"
# }

secret["username"]
# -> "my-username"
```
