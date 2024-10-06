# Secrecy Tutorial

The simplest way to get started is using the environment-variable-based
appraoch. Here, you configure named secrets using environment variables, and
then retrieve them using the `secrecy(name)` function in your code.

This section provides a few examples to give you a better idea how this looks
like. All examples will fetch a secret that contains database credentials, but
we'll use three different ways of storing them to show the flexibility that
secrecy provides.

### Retreiving Secrets In Code

Lets pretend, we already got some secrets stored _somewhere_, be it in a file,
AWS, the password manager of your choice, or a hand-written sticky note pinned
to your monitor.

This secret contains database credentials, and has the following entries:
- user: my-database-user
- password: s3cr3t-password-123
- host: abcxyz.us-east-1.mydatabaseprovider.com

Retrieving them in Python is as simple as the following

```python
# database.py
from secrecy.autoresolve.sync import secrecy

credentials = secrecy(name="my_database")

# In the real world, you would use something like the following:
#
# import mydb_driver
# connection = mydb_driver.connect(
#     user=credentials["user"],
#     password=credentials["password"],
#     host=credentials["host"],
# )
print("I would connect to the database using the following credentials:")
print(credentials)
```

Running the above file would yield the following output:

```
python database.py
I would connect to the database using the following credentials:
{
    "user": "my-database-user",
    "password": "s3cr3t-password-123",
    "host": "abcxyz.us-east-1.mydatabaseprovider.com"
}
```

As you can see the footprint of secrecy in the code is quite minimal. We only
call `secrecy(name="my_database")`, which returns a dictionary containing our
secret values.

The thing that is missing is how to teach secrecy where to find the physically
stored secrets and how to access them. This is explained in the following
sections, and is also a key motivation for why secrecy exists. There are
numerous ways of storing something in a secure way, each a little different
than the other. Secrecy tries to move all these difference into configuration,
so your code (and hopefully also your configration) can be simple.

Let's now look into how to actually store the secrets and setup the required
configuration in order for the above code to work.

### Encrypted Files

A simple way of storing our user, password and host values is to store them in
an encrypted file. This file can then be comitted to source control, and
thereby distributed to your coworkers or deployed to a server. You then have to
manage one password to encrypt and decrypt this file. This is not the most
robust way of doing things but it works regardless of whether you'll deploy
your application to Amazon, Google, or your own servers running in your
basement.

First need to install the right Python package, which in this case is
`secrecy_file`:

```shell
pip install secrecy-file
```

This includes hooks into the `secrecy` package, as well as a commandline
interface for managing adding, updating, or removing secrets in our file.

#### Creating The File

After installing the `secrecy-file` package, a script with the same name should
be available to us. You can verify that everything works as expected by
running.

```shell
secrecy-file --help
```

As described by the output, we can create an new file using

```
secrecy-file create my_database
Created a new empty secrets file in './secrets/my_database'!

Your encryption password is the following:

    cxNonMTxuCAjQNUM8pMMCeoK6_H3ozrChBAs5O01Q0k=

Make sure you store this somewhere secure and reliable! If you loose this, you
also loose access to your encrypted secrets!
```

Do what the output says.

We then can add new entries using the commands in the following form

```shell
secrecy-file --name=MY_SECRET_NAME --password=MY_PASSWORD add "key" "value"
```

This gets cumbersome quite easily. To make our lives easier, lets define two
environment variables in our shell, so we don't have to repeat the secret name
and password every time.

> [!NOTE]
> This might not work on Windows or if you use a non-POSIX compliant shell.
> Also, don't straight up copy paste these commands without replacing the
> `REPLACE_WITH_` part.

```shell
export SECRECY_FILE_NAME="my_database";
export SECRECY_FILE_PASSWORD="REPLACE_WITH_THE_PASSWORD_PRINTED_EARLIER";
```

We then can add all of our secrets from earlier

```shell
secrecy-file add user "my-database-user"
secrecy-file add password "s3cr3t-password-123"
secrecy-file add host "abcxyz.us-east-1.mydatabaseprovider.com"
```

To be sure, we can print all secrets to the console

```shell
secrecy-file show
```

#### Configuring Secrecy

Now on to the next part. If we run the `database.py` from earlier, we'll run
into the following error:

```
python database.py
TODO: REPLACE ME WITH THE ACTUAL ERROR OUTPUT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

As said earlier, secrecy moves much logic to the configuration layer, which is
done using environment variables. Configuring a secret for secrecy consists of
roughly three parts:

1. **The name of the secret.** This is passed implicitly, since all envirnoment
   variables for a specific secret are prefixed with
   `SECRECY_THENAME`. In our example, we called the secret `my_database`. By
   convention, environment variables are uppercase, so we prefix all of our
   environment variables with `SECRECY_MY_DATABASE`.
2. **The driver that determines _how_ the secrets will be retrieved.** This is
   the minimally required environment variable `SECRECY_THENAME_DRIVER`. We use
   `secrecy_file`, which according to its documentation uses the
   `encrypted_file` driver name. So we run
   ```shell
   export SECRECY_MY_DATABASE_DRIVER="encrypted_file";
   ```
   to set it for our current shell session.
3. **Any driver-specific configuration.** In our case, the file-based driver
   requires the password to decrypt the file, which is read from the
   `SECRECY_THENAME_PASSWORD`. We could run
   ```shell
   export SECRECY_MY_DATABASE_PASSWORD="REPLACE_WITH_THE_PASSWORD_PRINTED_EARLIER";
   ```
   to explicitly set the password only for the `my_database` secret. However,
   if the explicit environment variable is not present, `secrecy_file` attempts
   to read it from `SECRECY_FILE_PASSWORD`, which we set earlier. So ideally,
   we now don't need any driver-specific configuration.

After correctly setting up the environment, we can run our `database.py` again,
to verify that it now works as promised earlier:

```
python database.py
I would connect to the database using the following credentials:
{
    "user": "my-database-user",
    "password": "s3cr3t-password-123",
    "host": "abcxyz.us-east-1.mydatabaseprovider.com"
}
```

#### Drawbacks

First of all: yay, we successfully stored our secret!  But, as you may noticed,
we now need to manage an additional secret: the password to our encrypted file.
One could argue, that we now only need to manage a single secret, which unlocks
multiple ones, and this may be all you need. However, you may already have an
account with your deployment provider, which may also provide some way of
storing secrets. In that case, you likely want to re-use your account. This
usually also comes with other benefits, like fine-grained access control or
automated rotation mechanisms.

The next section uses Amazons Secrets Manager, but the necessary steps for
setting things up should be similar for GCP, or whatever else you use. You
only need to change some configuration parameters and install the fitting
package.

### Amazon Secrets Manager

Imagine you deploy `database.py` as a Lambda function. You could manually copy
and use the [examples provided by Amazon](https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets-python-sdk.html).

You could also use `secrecy-aws`, set up

```dotenv
SECRECY_MY_DATABASE_DRIVER="aws-secretsmanager"
```

as an environment variable through the AWS Console or CDK, and everything
should work as expected.

### 1password

```shell
pip install secrecy-onepassword
```

### In-Memory



### Outlook

- Also push and change secrets programmatically
- manually build specific secret sources
- A link or a list to different `secrecy_X` implementations for common use-cases
