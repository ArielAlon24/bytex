from typing import Callable

from bytex.bits import BitBuffer
from bytex.endianness import Endianness
from bytex.errors import ParsingError
from bytex.structure.types import Fields


def _create_parse(
    fields: Fields,
) -> Callable[[object, bytes, Endianness, bool], object]:
    @classmethod  # type: ignore[misc]
    def parse(
        cls,
        data: bytes,
        endianness: Endianness = Endianness.LITTLE,
        strict: bool = False,
    ) -> object:
        buffer = BitBuffer.from_bytes(data)
        values = {}

        for name, field in fields.items():
            values[name] = field.codec.deserialize(buffer, endianness=endianness)

        if strict and len(buffer):
            raise ParsingError(f"Unexpected trailing data: {len(buffer)} bits left")

        return cls(**values)

    return parse
