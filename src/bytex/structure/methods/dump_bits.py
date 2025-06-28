from typing import Callable

from bytex.structure.types import Fields
from bytex.bits import Bits, BitBuffer


def _create_dump_bits(fields: Fields) -> Callable[[object], Bits]:
    def dump_bits(self) -> Bits:
        buffer = BitBuffer()

        for name, field in fields.items():
            value = getattr(self, name)
            buffer.write(field.codec.serialize(value))

        return buffer.to_bits()

    return dump_bits
