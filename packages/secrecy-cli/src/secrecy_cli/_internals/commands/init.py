import subprocess
from enum import StrEnum
from os import getcwd, listdir
from pathlib import Path

import click
import tomllib
from pick import pick


@click.command()
@click.option(
    "--module",
    default=None,
    help="A path to the module where the file containing the secrets should be placed",
)
def init(module: str | None):
    """Run through the initialization process.

    This consists of setting up a `secrets.py` file, defining a default source,
    and optionally installing additional first-party sources.
    """
    cwd = Path(getcwd())
    module_dir = _get_valid_module_dir(cwd, module)

    selected_sources = _recommend_sources()
    package_manager = _infer_package_manager(cwd)
    _install_drivers(package_manager, selected_sources)

    created_file = _create_secrets_py(directory=module_dir, sources=selected_sources)
    if created_file is None:
        return

    relative_created = created_file.relative_to(cwd)
    click.echo(
        "Created " + click.style(relative_created, fg="green", bold=True), err=True
    )


def _get_valid_module_dir(cwd: Path, explicit_module: str | None) -> Path:
    """Returns a path to the module, where we should initialize"""
    if explicit_module:
        explicit_path = Path(explicit_module)
        if not explicit_path.exists():
            raise ValueError(f"'{explicit_module}' does not exist")
        return explicit_path

    return _infer_main_module_dir(cwd)


def _infer_main_module_dir(root: Path) -> Path:
    # This is the common layout, where python just adds the current directory to the path.
    root_as_package = root / root.name.lower().replace("-", "_")
    if _is_python_module(root_as_package):
        return root_as_package

    pyproject = root / "pyproject.toml"
    explicit_name = (
        tomllib.loads(pyproject.read_text()).get("project", {}).get("name", None)
    )
    if explicit_name:
        explicit_as_module = root / explicit_name.replace("-", "_")
        if _is_python_module(explicit_as_module):
            return explicit_as_module

    # This is also pretty popular, e.g. in FastAPI projects
    if _is_python_module(root / "app"):
        return root / "app"

    src = root / "src"
    if src.exists() and src.is_dir():
        src_packages = listdir(src)
        if len(src_packages) == 1:
            only_module = src / src_packages[0]
            if _is_python_module(only_module):
                return only_module

    # If everything fails, simply place the file at the cwd
    return root


def _is_python_module(path: Path) -> bool:
    return path.is_dir() and (path / "__init__.py").is_file()


def _recommend_sources() -> list[str]:
    result: list[tuple[str, int]] = pick(
        title="Select a source using <space>, confirm your selection with <enter>",
        clear_screen=False,
        options=list(DEFAULT_SOURCES_BY_PACKAGE.keys()),
        multiselect=True,
    )

    return [option for option, _ in result]


class PackageManager(StrEnum):
    PIP = "pip"
    """https://pip.pypa.io"""
    UV = "uv"
    """https://docs.astral.sh/uv"""
    POETRY = "poetry"
    """https://python-poetry.org"""
    PDM = "pdm"
    """https://pdm-project.org"""


# TODO: Write a test for this mapping
DEFAULT_SOURCES_BY_PACKAGE = {
    "secrecy-aws": "SecretsManagerSource",
    # "secrecy-azure": "",
    # "secrecy-docker",
    # "secrecy-environment",
    # "secrecy-file",
    # "secrecy-google-cloud",
    # "secrecy-onepassword",
}


def _infer_package_manager(
    cwd: Path,
) -> PackageManager:
    # These are quite cheap to check
    if (cwd / "uv.lock").is_file():
        return PackageManager.UV
    if (cwd / "poetry.lock").is_file():
        return PackageManager.POETRY
    if (cwd / "pdm.lock").is_file():
        return PackageManager.UV

    # Maybe we find more in the pyproject config
    pyproject = cwd / "pyproject.toml"
    pyproject = tomllib.loads(pyproject.read_text()) if pyproject.is_file() else {}
    tools = pyproject.get("tool", {})
    if "uv" in tools:
        return PackageManager.UV
    if "poetry" in tools:
        return PackageManager.POETRY
    if "pdm" in tools:
        return PackageManager.UV

    # A default check for UV, which may not be enough, but should work most of the time.
    # UV is the only package manager (I know of) that defaults to not shipping pip with
    # their venvs, so here we need to check before defaulting to pip.
    uv_venv = cwd / ".venv"
    if uv_venv.is_dir() and not uv_venv / "bin" / "pip":
        return PackageManager.UV

    # If everything else fails, just assume PIP
    return PackageManager.PIP


def _install_drivers(package_manager: PackageManager, packages: list[str]) -> None:
    if len(packages) == 0:
        return

    verb = "install" if package_manager is PackageManager.PIP else "add"
    cmdline = subprocess.list2cmdline([str(package_manager), verb, *packages])
    click.echo(cmdline, err=True)
    subprocess.run(cmdline, shell=True, check=True)


def _create_secrets_py(
    directory: Path,
    sources: list[str],
) -> Path | None:
    lines = ["from secrecy import Secret, register_source"]

    for source_package in sources:
        source_module = source_package.replace("-", "_")
        default_source_class = DEFAULT_SOURCES_BY_PACKAGE[source_package]
        lines.append(f"from {source_module} import {default_source_class}")
    lines.append("")

    for index, source_package in enumerate(sources):
        default_source_class = DEFAULT_SOURCES_BY_PACKAGE[source_package]
        source_name = source_package.removeprefix("secrecy-")
        if index == 0:
            lines.append(
                f'register_source("{source_name}", {default_source_class}, default=True)'
            )
        else:
            lines.append(f'register_source("{source_name}", {default_source_class})')
    lines.append("")

    lines += [
        "# These for demonstration purposes only. Feel free to replace them with your own secrets.",
        'api_token = Secret("api_token")',
        'db_credentials = Secret("db_credentials")',
        "",
    ]
    file_path = directory / "secrets.py"

    if file_path.exists():
        if not click.confirm(
            f"'{file_path}' already exists, do you want to override it?"
        ):
            return None

    file_path.write_text("\n".join(lines))
    return file_path
