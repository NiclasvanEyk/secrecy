"""Load statically defined secrets in an application."""

from importlib import import_module

from secrecy.secret import Secret


def discover_secrets_in(modules: set[str]) -> list[Secret]:
    """
    Imports all given modules and returns the top-level`Secret`s.

    Variable names starting with "_" are ignored.
    """

    secrets = []
    for module_specifier in modules:
        for name, instance in import_module(module_specifier).__dict__.items():
            if name.startswith("_"):
                continue

            if isinstance(instance, Secret):
                secrets.append(instance)

    return secrets
