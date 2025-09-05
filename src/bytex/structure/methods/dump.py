from typing import Callable

from bytex.bits import BitBuffer
from bytex.endianness import Endianness
from bytex.errors import AlignmentError
from bytex.structure.types import Fields


def _create_dump(fields: Fields) -> Callable[[object, Endianness], bytes]:
    def dump(self, endianness: Endianness = Endianness.LITTLE) -> bytes:
        buffer = BitBuffer()
        for name, field in fields.items():
            value = getattr(self, name)
            buffer.write(field.codec.serialize(value, endianness=endianness))

        try:
            return buffer.to_bytes()
        except AlignmentError as e:
            raise AlignmentError(
                "Cannot dump a structure whose bit size is not a multiple of 8"
            ) from e

    return dump
