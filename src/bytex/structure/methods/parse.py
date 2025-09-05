from typing import Callable

from bytex.bits import BitBuffer
from bytex.endianes import Endianes
from bytex.errors import ParsingError
from bytex.structure.types import Fields


def _create_parse(fields: Fields) -> Callable[[object, bytes, Endianes, bool], object]:
    @classmethod  # type: ignore[misc]
    def parse(
        cls, data: bytes, endianes: Endianes = Endianes.LITTLE, strict: bool = False
    ) -> object:
        buffer = BitBuffer.from_bytes(data)
        values = {}

        for name, field in fields.items():
            values[name] = field.codec.deserialize(buffer, endianes=endianes)

        if strict and len(buffer):
            raise ParsingError(f"Unexpected trailing data: {len(buffer)} bits left")

        return cls(**values)

    return parse
