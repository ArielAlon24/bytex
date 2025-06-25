from typing import Callable

from bytex._structure.types import Codecs
from bytex.bits import Bits, BitBuffer


def _create_dump_bits(codecs: Codecs) -> Callable[[object], Bits]:
    def dump_bits(self) -> Bits:
        buffer = BitBuffer()

        for name, codec in codecs.items():
            value = getattr(self, name)
            buffer.write(codec.serialize(value))

        return buffer.to_bits()

    return dump_bits
