from typing import Callable

from bytex._structure.types import Codecs
from bytex.bits import BitBuffer
from bytex.errors import StructureError, ParsingError


def _create_parse_bits(
    codecs: Codecs,
) -> Callable[[object, BitBuffer, bool], object]:
    @classmethod  # type: ignore[misc]
    def parse_bits(
        cls,
        buffer: BitBuffer,
        strict: bool = False,
    ) -> object:
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

    return parse_bits
