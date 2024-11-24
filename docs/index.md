# Secrecy

Properly handling secrets can be cumbersome.
To make things worse, it is not an _essential_ requirement for working software.
Combine both of these, and it is likely to be skipped, or put in a ticket that rots away in your ever growing backlog of tasks.

**Secrecy** aims to make secrets simple.
No matter if you store them in your [cloud providers secret store](./ecosystem/index.md#cloud-providers), your [password manager](./ecosystem/index.md#password-managers), or simply in [an encrypted file](./ecosystem/index.md#simple-solutions) that gets checked in with your code.

Secrecy provides a simple and unified API to retrieve secrets:

```python hl_lines="1 4"
from secrecy import fetch_secret
from my_app.database import connect_to_db

db_secrets = fetch_secret(name="database_credentials")
db_connection = connect_to_db(url=db_secrets["url"])
```

No matter if you store your secrets in
[a file in an encrypted file](./ecosystem/simple_solutions/encrypted_files.md),
in [your hosting platforms secret store](./ecosystem/cloud_providers/aws.md),
or as [environment variables](./ecosystem/simple_solutions/environment_variables.md)
– the above code would not change.
Everything gets configured outside of your source code, so you can use different providers when developing locally than e.g. on your staging or production environment.

If you just want to get going,  Head over to the [ecosystem overview](./ecosystem/index.md).
Otherwise, it is recommended to get to know
