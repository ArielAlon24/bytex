from typing import Callable

from bytex.bits import BitBuffer
from bytex.endianness import Endianness
from bytex.errors import ParsingError, StructureError
from bytex.structure.types import Fields


def _create_parse_bits(
    fields: Fields,
) -> Callable[[object, BitBuffer, Endianness, bool], object]:
    @classmethod  # type: ignore[misc]
    def parse_bits(
        cls,
        buffer: BitBuffer,
        endianness: Endianness,
        strict: bool = False,
    ) -> object:
        values = {}

        for name, field in fields.items():
            try:
                values[name] = field.codec.deserialize(buffer, endianness=endianness)
            except StructureError as e:
                raise ParsingError(
                    f"Insufficient data while parsing field '{name}'"
                ) from e

        if strict and len(buffer):
            raise ParsingError(f"Unexpected trailing data: {len(buffer)} bits left")

        return cls(**values)

    return parse_bits
