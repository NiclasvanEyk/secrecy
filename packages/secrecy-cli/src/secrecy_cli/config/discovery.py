from pathlib import Path
from typing import Any

from secrecy.exception import SecrecyError
from tomllib import load

from secrecy_cli.config.schema import SecrecyCliConfig

ParsedTomlValues = dict[str, Any]


def discover_pyproject_path(cwd: Path | None = None) -> Path | None:
    if cwd is None:
        cwd = Path.cwd()

    cwd_pyproject = cwd / "pyproject.toml"
    if cwd_pyproject.exists():
        return cwd_pyproject

    # TODO: Maybe recurse upwards the directory tree.
    return None


def load_pyproject_from(pyproject: Path) -> ParsedTomlValues:
    with pyproject.open("rb") as project_config_file:
        return load(project_config_file)


def parse_secrecy_tool_config(pyproject_config: ParsedTomlValues) -> SecrecyCliConfig:
    tools = pyproject_config.get("tool")
    if not isinstance(tools, dict):
        tools = {}

    secrecy_config = tools.get("secrecy")
    if secrecy_config is None:
        return SecrecyCliConfig.default()

    if not isinstance(secrecy_config, dict):
        raise SecrecyError("Secrecy config is not a dict!")

    return SecrecyCliConfig.model_validate(secrecy_config)


def resolve_config() -> SecrecyCliConfig:
    project_config_path = discover_pyproject_path()
    if project_config_path is None:
        return SecrecyCliConfig.default()

    raw_config = load_pyproject_from(project_config_path)
    return parse_secrecy_tool_config(raw_config)
