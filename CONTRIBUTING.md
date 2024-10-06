# Contributing

## Package Management

This monorepo uses [uv](https://docs.astral.sh/uv/) to manage

## Creating A New Package

Create a new package using uv.

```shell
cd packages
uv init --package --lib --no-pin-python --vcs=none secrecy-MYNEWPACKAGE
```

Setup the dependency on the `secrecy` package.

```diff
[project]
name = "secrecy-mynewpackage"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
-dependencies = []
+dependencies = ["secrecy"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
+
+[tool.uv.sources]
+secrecy = { workspace = true }
```

Populate the package `README.md` and add an entry to the
ecosystem section [`README.md` of the repository](./README.md#ecosystem).