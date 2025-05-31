from typing import Any, Callable, Dict, Set, Type
from typing_extensions import ParamSpec, ParamSpecKwargs

from structure._structure.types import Codecs
from structure.bit_buffer import BitBuffer
from structure.endianes import Endianes
from structure.errors import (
    AlignmentError,
    ParsingError,
    StructureError,
    ValidationError,
)
from structure.field import Field


def _create_init(codecs: Codecs) -> Callable[[object], None]:
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


def _create_repr(codecs: Codecs) -> Callable[[object], str]:
    def __repr__(self) -> str:
        result = f"{self.__class__.__name__}("

        for index, (name, codec) in enumerate(codecs.items()):
            value = getattr(self, name)

            if index == 0:
                result += f"{name}: {codec} = {value}"
            else:
                result += f", {name}: {codec} = {value}"

        return f"{result})"

    return __repr__


def _create_dump(codecs: Codecs) -> Callable[[object, Endianes], bytes]:
    def dump(self, endianes: Endianes = Endianes.LITTLE) -> bytes:
        if sum(field.bit_remainder() for field in codecs.values()) % 8 != 0:
            raise AlignmentError(
                "Cannot dump a structure whose bit size is not a multiple of 8"
            )

        buffer = BitBuffer()
        for name, codec in codecs.items():
            value = getattr(self, name)
            buffer.write(codec.serialize(value))

        return buffer.to_bytes(endianes=endianes)

    return dump


def _create_parse(codecs: Codecs) -> Callable[[type, bytes, Endianes], object]:
    @classmethod
    def parse(
        cls, data: bytes, endianes: Endianes = Endianes.LITTLE, strict: bool = False
    ) -> object:
        buffer = BitBuffer.from_bytes(data, endianes=endianes)
        values = {}

        for name, codec in codecs.items():
            try:
                values[name] = codec.deserialize(buffer)
            except StructureError as e:
                raise ParsingError(
                    f"Insufficient data while parsing field '{name}'"
                ) from e

        if strict and len(buffer):
            raise ParsingError(f"Unexpected trailing data: {len(buffer)} bits left")

        return cls(**values)

    return parse
