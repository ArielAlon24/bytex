from typing import Callable

from bytex.bits import BitBuffer, Bits
from bytex.endianness import Endianness
from bytex.structure.types import Fields


def _create_dump_bits(fields: Fields) -> Callable[[object, Endianness], Bits]:
    def dump_bits(self, endianness: Endianness) -> Bits:
        buffer = BitBuffer()

        for name, field in fields.items():
            value = getattr(self, name)
            buffer.write(field.codec.serialize(value, endianness=endianness))

        return buffer.to_bits()

    return dump_bits
