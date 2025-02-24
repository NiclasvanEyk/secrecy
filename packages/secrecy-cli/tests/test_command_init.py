from collections.abc import Iterable
from pathlib import Path

from secrecy_cli._internals.commands.init import _get_valid_module_dir


def test_it_can_infer_the_module_through_dir_name(
    tmp_path: Path,
) -> None:
    file_tree(
        tmp_path,
        {
            "secrecy-command_tests-init": {
                "secrecy_command_tests_init": {
                    "__init__.py": "",
                },
            },
        },
    )
    base = tmp_path / "secrecy-command_tests-init"
    inferred_module = _get_valid_module_dir(base, None)
    assert inferred_module == base / "secrecy_command_tests_init"


def test_it_can_infer_the_module_through_pyproject_toml_name(
    tmp_path: Path,
) -> None:
    file_tree(
        tmp_path,
        {
            "pyproject.toml": (
                "[project]",
                'name = "secrecy-command-tests-init"',
                'version = "0.1.0"',
            ),
            "secrecy_command_tests_init": {
                "__init__.py": "",
            },
        },
    )
    inferred_module = _get_valid_module_dir(tmp_path, None)
    assert inferred_module == tmp_path / "secrecy_command_tests_init"


def test_it_can_infer_the_module_through_pyproject_toml_with_src(
    tmp_path: Path,
) -> None:
    file_tree(
        tmp_path,
        {
            "pyproject.toml": (
                "[project]",
                'name = "secrecy-command-tests-init"',
                'version = "0.1.0"',
            ),
            "src": {
                "secrecy_command_tests_init": {
                    "__init__.py": "",
                }
            },
        },
    )

    inferred_module = _get_valid_module_dir(tmp_path, None)
    assert inferred_module == tmp_path / "src" / "secrecy_command_tests_init"


# -------------------------------------------------------------------------------------


type FileTree = dict[str, str | Iterable[str] | FileTree]


def file_tree(path: Path, tree: FileTree) -> None:
    for file_name, contents in tree.items():
        if isinstance(contents, dict):
            (path / file_name).mkdir()
            file_tree(path / file_name, contents)
            continue

        (path / file_name).write_text(
            contents if isinstance(contents, str) else "\n".join(contents)
        )
