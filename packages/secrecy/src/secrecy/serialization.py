import json

from secrecy._internals.core import JSON, Definition

supports_pydantic = False
try:
    from pydantic import BaseModel

    supports_pydantic = True
except ImportError:
    supports_pydantic = False


def serialize_from_string[T](
    definition: Definition[T],
    raw_value: str,
) -> T:
    if definition.shape is str:
        return raw_value

    if supports_pydantic and issubclass(definition.shape, BaseModel):
        return definition.shape.model_validate_json(raw_value)

    if definition.shape is dict or definition.shape is JSON:
        return json.loads(raw_value)

    if definition.shape is int:
        return int(raw_value)

    if definition.shape is float:
        return float(raw_value)

    raise ValueError(f"Unsupported serialization format: {definition.shape}")
