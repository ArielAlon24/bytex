from typing import Callable

from bytex.structure.types import Fields
from bytex.endianes import Endianes
from bytex.bits import BitBuffer
from bytex.errors import ParsingError


def _create_parse(fields: Fields) -> Callable[[object, bytes, Endianes, bool], object]:
    @classmethod  # type: ignore[misc]
    def parse(
        cls, data: bytes, endianes: Endianes = Endianes.LITTLE, strict: bool = False
    ) -> object:
        buffer = BitBuffer.from_bytes(data, endianes=endianes)
        values = {}

        for name, field in fields.items():
            values[name] = field.codec.deserialize(buffer)

        if strict and len(buffer):
            raise ParsingError(f"Unexpected trailing data: {len(buffer)} bits left")

        return cls(**values)

    return parse
