# Ecosystem

There are a thousand ways to store a secret, you just got to choose one.

## Simple Solutions

- [`secrecy-file`](./packages/secrecy-file) – Store your secrets in an encrypted file.
- [`secrecy-environment`](./packages/secrecy-environment) – Store your secrets as environment variables.

## Cloud Providers

If you already use a cloud provider like AWS, GCP, or Azure, it makes sense to
also use their secret management solution.

- [`secrecy-aws`](./cloud_providers/aws.md) – Store your secrets in the [AWS Secrets Manager](https://aws.amazon.com/de/secrets-manager).
- [`secrecy-azure`](./cloud_providers/azure.md) – Store your secrets in the [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault).
- [`secrecy-google-cloud`](./cloud_providers/google_cloud.md) – Store your secrets in the [Google Cloud Secret Manager](https://cloud.google.com/secret-manager).

## Password Managers

Do you already use a password manager? Maybe also use it to manage your secrets!

- [`secrecy-onepassword`](./password_managers/onepassword.md) – Manage your secrets in 1Password.

## Containers

- [`secrecy-docker`](./packages/secrecy-docker) – Support for [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/) or [Podman Secrets](https://docs.podman.io/en/latest/markdown/podman-secret-create.1.html)
