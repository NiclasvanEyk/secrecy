# Secrecy for Amazon Web Services (AWS)

## Getting Started

Install the package from PyPi

```shell
pip install secrecy-aws
```

Then create a secret, if this was not already doneA.

Then in the Python file you want to use

<!-- SECRECY_USAGE_EXAMPLE -->
```python
from secrecy.autoresolve.sync import secrecy

secret = secrecy("db_credentials")
```
