from importlib import import_module
from types import ModuleType
from typing import Any

from secrecy.exception import SecrecyError

MEMBER_DOES_NOT_EXIST = object()


def import_dotted_path(path: str) -> tuple[ModuleType, Any]:
    """Dynamically imports something from a module via dotted path notation.

    Sometimes we want to refer to a specific function or variable from a python module through a string.
    E.g. you may want to run an ASGI app using the popular `uvicorn` server, and in order to do that, you
    need to tell the `uvicorn` CLI where your ASGI app variable lives. Then you'd run something like

    ```shell
    uvicorn my_app.http.server:app
    ```

    where `my_app.http.server` is the python module, and `app` the variable name in that module that
    represents your ASGI app.

    We mostly use this for driver functions.
    """
    path_to_module, member_name = path.split(":")
    module = import_module(path_to_module)

    member = getattr(module, member_name, MEMBER_DOES_NOT_EXIST)
    if member is MEMBER_DOES_NOT_EXIST:
        raise SecrecyError(
            f"Module {path_to_module} does not contain an '{member_name}' object"
        )

    return module, member
