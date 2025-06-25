from typing import Callable

from bytex._structure.types import Codecs
from bytex.endianes import Endianes
from bytex.bits import BitBuffer
from bytex.errors import ParsingError


def _create_parse(codecs: Codecs) -> Callable[[object, bytes, Endianes, bool], object]:
    @classmethod  # type: ignore[misc]
    def parse(
        cls, data: bytes, endianes: Endianes = Endianes.LITTLE, strict: bool = False
    ) -> object:
        buffer = BitBuffer.from_bytes(data, endianes=endianes)
        values = {}

        for name, codec in codecs.items():
            values[name] = codec.deserialize(buffer)

        if strict and len(buffer):
            raise ParsingError(f"Unexpected trailing data: {len(buffer)} bits left")

        return cls(**values)

    return parse
