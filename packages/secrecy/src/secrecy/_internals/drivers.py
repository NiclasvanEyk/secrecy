from dataclasses import dataclass
from importlib.metadata import entry_points
from typing import final

from secrecy.exception import SecrecyError


@final
@dataclass(frozen=True, slots=True)
class Driver:
    name: str
    """A user-facing name.

    This acts as a layer of indirection, to allow driver authors to have a
    bit more freedom to refactor drivers.
    """

    module: str
    """Path to the python module that contains the driver function."""

    member: str
    """Name of the driver function."""

    @property
    def dotted_path(self) -> str:
        """A dotted path to the module and member."""
        return f"{self.module}:{self.member}"


def discover_drivers() -> list[Driver]:
    """Discovers all secrecy drivers from importlibs metadata."""
    drivers: list[Driver] = []
    for entry in entry_points(group="secrecy.driver"):
        parts = entry.value.split(":")
        if len(parts) != 2:
            raise SecrecyError(
                f"Malformed driver name '{entry.name}'! Drivers should contain exactly one ':'."
            )

        module, member = parts
        drivers.append(Driver(name=entry.name, module=module, member=member))

    return drivers
