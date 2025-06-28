from re import I
from typing import Any, Callable, Dict, Set

from bytex.structure.types import Fields
from bytex.errors import ValidationError
from bytex.field import Field


def _create_init(fields: Fields) -> Callable[..., None]:
    def __init__(self: object, **data: Any) -> None:
        _validate_keys(actual_keys=set(data.keys()), fields=fields)

        for name, field in fields.items():
            if name in data:
                value = data[name]
            elif field.default is not None:
                value = field.default
            else:
                raise ValidationError("Unreachable")

            setattr(self, name, value)

    return __init__


def _format_key_error_message(keys: Set[str], kind: str) -> str:
    label = "field" if len(keys) == 1 else "fields"
    keys_str = ", ".join(repr(k) for k in sorted(keys))
    return f"{kind} {label}: {keys_str}"


def _validate_keys(actual_keys: Set[str], fields: Dict[str, Field]) -> None:
    default_keys = {name for name, field in fields.items() if field.default is not None}
    expected_keys = set(fields.keys())
    required_keys = expected_keys - default_keys
    missing_keys = required_keys - actual_keys
    unexpected_keys = actual_keys - expected_keys

    if not missing_keys and not unexpected_keys:
        return

    messages = []
    if missing_keys:
        messages.append(_format_key_error_message(missing_keys, "Missing"))
    if unexpected_keys:
        messages.append(_format_key_error_message(unexpected_keys, "Unexpected"))

    raise ValidationError("Invalid constructor arguments - " + "; ".join(messages))
