from typing import Callable

from bytex.bits import BitBuffer, Bits
from bytex.endianes import Endianes
from bytex.structure.types import Fields


def _create_dump_bits(fields: Fields) -> Callable[[object, Endianes], Bits]:
    def dump_bits(self, endianes: Endianes) -> Bits:
        buffer = BitBuffer()

        for name, field in fields.items():
            value = getattr(self, name)
            buffer.write(field.codec.serialize(value, endianes=endianes))

        return buffer.to_bits()

    return dump_bits
