# Secrecy

This is the Secrecy monorepo. It contains all first-party code

If you are interested what Secrecy can offer you, have a look at [the Tutorial](./TUTORIAL.md).

## Ecosystem

There are a thousand ways to store a secret, you just got to choose one.

### Simple Solutions

- [`secrecy-file`](./packages/secrecy-file) – Store your secrets in an encrypted file.

### Cloud Providers

If you already use a cloud provider like AWS, GCP, or Azure, it makes sense to
also use their secret management solution.

- [`secrecy-aws`](./packages/secrecy-aws) – Store your secrets in the [AWS Secrets Manager](https://aws.amazon.com/de/secrets-manager).
- [`secrecy-google-cloud`](./packages/secrecy-google-cloud) – Store your secrets in the [Google Cloud Secret Manager](https://cloud.google.com/secret-manager).

### Password Managers

Do you already use a password manager? Maybe also use it to manage your secrets!

- [`secrecy-onepassword`](./packages/secrecy-onepassword) – Manage your secrets in 1Password.

### Other

- [`secrecy-environment`](./packages/secrecy-environment) – Store your secrets as envrionment variables.

## Concepts

### Secret Names

> [!IMPORTANT]
> Talk about secret names and how they appear in environment variables.
