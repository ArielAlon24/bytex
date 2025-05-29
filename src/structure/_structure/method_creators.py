from typing import Any, Callable, Dict, Set, Type
from typing_extensions import ParamSpec, ParamSpecKwargs

from structure._structure.types import Fields
from structure.bit_buffer import BitBuffer
from structure.endianes import Endianes
from structure.data_types.base_data_type import BaseDataType
from structure.data_types.integer import Integer
from structure.codecs.base_codec import BaseCodec
from structure.codecs.integer import IntegerCodec
from structure.errors import (
    AlignmentError,
    ParsingError,
    StructureError,
    ValidationError,
)

CODECS_DATA_TYPES: Dict[Type[BaseCodec], Type[BaseDataType]] = {IntegerCodec: Integer}


def _create_init(fields: Fields) -> Callable[[object], None]:
    def __init__(self: object, **data: Any) -> None:
        _validate_keys(expected_keys=set(fields.keys()), actual_keys=set(data.keys()))

        for field_name, codec in fields.items():
            value = data.get(field_name)
            data_type_class = CODECS_DATA_TYPES[type(codec)]

            if value is None:
                raise ValidationError("Unreachable!")

            setattr(self, field_name, data_type_class(codec=codec, value=value))

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


def _create_repr(fields: Fields) -> Callable[[object], str]:
    def __repr__(self) -> str:
        result = f"{self.__class__.__name__}("

        for index, (field_name, codec) in enumerate(fields.items()):
            value = getattr(self, field_name)

            if index == 0:
                result += f"{field_name}: {codec} = {value}"
            else:
                result += f", {field_name}: {codec} = {value}"

        return f"{result})"

    return __repr__


def _create_dump(fields: Fields) -> Callable[[object, Endianes], bytes]:
    def dump(self, endianes: Endianes = Endianes.LITTLE) -> bytes:
        if sum(field.bit_remainder() for field in fields.values()) % 8 != 0:
            raise AlignmentError(
                "Cannot dump a structure whose bit size is not a multiple of 8"
            )

        buffer = BitBuffer()
        for field_name, codec in fields.items():
            value = getattr(self, field_name)
            buffer.write(codec.serialize(value))

        return buffer.to_bytes(endianes=endianes)

    return dump


def _create_parse(fields: Fields) -> Callable[[type, bytes, Endianes], object]:
    @classmethod
    def parse(
        cls, data: bytes, endianes: Endianes = Endianes.LITTLE, strict: bool = False
    ) -> object:
        buffer = BitBuffer.from_bytes(data, endianes=endianes)
        values = {}

        for field_name, codec in fields.items():
            try:
                values[field_name] = codec.deserialize(buffer)
            except StructureError as e:
                raise ParsingError(
                    f"Insufficient data while parsing field '{field_name}'"
                ) from e

        if strict and len(buffer):
            raise ParsingError(f"Unexpected trailing data: {len(buffer)} bits left")

        return cls(**values)

    return parse
