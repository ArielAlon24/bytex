from typing import Any, Callable, Set

from bytex._structure.types import Codecs
from bytex.errors import ValidationError
from bytex.field import Field


def _create_init(codecs: Codecs) -> Callable[..., None]:
    def __init__(self: object, **data: Any) -> None:
        _validate_keys(expected_keys=set(codecs.keys()), actual_keys=set(data.keys()))

        for name, codec in codecs.items():
            value = data.get(name)

            if value is None:
                raise ValidationError("Unreachable!")

            setattr(
                self.__class__,
                name,
                Field(codec=codec, name=name),
            )
            setattr(self, name, value)

    return __init__


def _format_key_error_message(keys: Set[str], kind: str) -> str:
    label = "field" if len(keys) == 1 else "fields"
    keys_str = ", ".join(repr(k) for k in sorted(keys))
    return f"{kind} {label}: {keys_str}"


def _validate_keys(expected_keys: Set[str], actual_keys: Set[str]) -> None:
    missing_keys = expected_keys - actual_keys
    unexpected_keys = actual_keys - expected_keys

    if not missing_keys and not unexpected_keys:
        return

    messages = []
    if missing_keys:
        messages.append(_format_key_error_message(missing_keys, "Missing"))
    if unexpected_keys:
        messages.append(_format_key_error_message(unexpected_keys, "Unexpected"))

    raise ValidationError("Invalid constructor arguments - " + "; ".join(messages))
