from typing import Callable

from structure._structure.types import Codecs
from structure.endianes import Endianes
from structure.bits import BitBuffer
from structure.errors import ParsingError


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
