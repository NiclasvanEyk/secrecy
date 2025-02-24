from enum import StrEnum


class OutputFormat(StrEnum):
    """What format we should use when printing output to the console."""

    TEXT = "text"
    """Regular textual output for humans."""

    JSON = "json"
    """Structured JSON output for tools."""
