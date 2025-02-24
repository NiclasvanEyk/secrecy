from dataclasses import dataclass
from enum import StrEnum
from os import getcwd, listdir
from pathlib import Path

import click
import tomllib


@click.command()
# TODO:
@click.option("--module", default=None)
@click.option("--no-docs", is_flag=True, default=False)
@click.option("--no-examples", is_flag=True, default=False)
@click.option("--bare", is_flag=True, default=False)
def init(module: str | None, no_docs: bool, no_examples: bool, bare: bool):
    """Run through the initialization process.

    This consists of setting up a `secrets.py` file, defining a default source,
    and optionally installing additional first-party sources.
    """
    # This reads horrible, but this way it is easier to opt-out of the boilerplate.
    add_docs = not no_docs
    if bare:
        add_docs = False
    add_examples = not no_examples
    if bare:
        add_examples = False

    cwd = Path(getcwd())
    module_dir = _get_valid_module_dir(cwd, module)

    # TODO: Recommend sources
    _recommend_drivers()

    created_file = _create_secrets_py(
        directory=module_dir,
        docs=add_docs,
        examples=add_examples,
        default_source=DefaultSource(
            name="default",
            module="secrecy_demo_source",
            type="DemoSource",
        ),
    )
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


def _recommend_drivers() -> None:
    """"""


class PackageManager(StrEnum):
    PIP = "pip"
    """https://pip.pypa.io"""
    UV = "uv"
    """https://docs.astral.sh/uv"""
    POETRY = "poetry"
    """https://python-poetry.org"""
    PDM = "pdm"
    """https://pdm-project.org"""


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


def _install_drivers(
    package_manager: PackageManager,
    packages: list[str],
) -> None:
    pass


def _prompt_default_source() -> str:
    """"""


@dataclass
class DefaultSource:
    name: str
    module: str
    type: str


def _create_secrets_py(
    directory: Path,
    default_source: DefaultSource | None,
    docs: bool,
    examples: bool,
) -> Path | None:
    contents = (
        f"""
from secrecy import Secret, register_source
from {default_source.module} import {default_source.type}

# TODO: Link to the relevant docs
register_source("{default_source.name}", {default_source.type}, default=True)

# These for demonstration purposes only. Feel free to replace them with your own secrets.
api_token = Secret("api_token")
db_credentials = Secret("db_credentials")

# To use these,
""".strip()
        + "\n"
    )
    file_path = directory / "secrets.py"

    if file_path.exists():
        click.echo(
            f"'{file_path}' already exists, do you want to override it? [y/N]: ",
            nl=False,
        )
        choice = click.getchar()
        click.echo()
        if choice.lower() != "y":
            click.echo("Aborting...")
            return None

    file_path.write_text(contents)
    return file_path
