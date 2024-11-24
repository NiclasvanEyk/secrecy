new package:
  uv init --directory=packages --package --lib --no-pin-python --vcs=none secrecy-{{package}}
  echo "\n[tool.uv.sources]" >> packages/secrecy-{{package}}/pyproject.toml
  echo "secrecy = { workspace = true }" >> packages/secrecy-{{package}}/pyproject.toml
  uv add --package=secrecy-{{package}} secrecy

docs:
   uv run mkdocs serve
