from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits, from_bits, to_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError


@dataclass(frozen=True)
class DataCodec(BaseCodec[bytes]):
    def validate(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(bytes)}'"
            )

    def serialize(self, value: bytes, endianness: Endianness) -> Bits:
        return to_bits(value, endianness=endianness)

    def deserialize(self, bit_buffer: BitBuffer, endianness: Endianness) -> bytes:
        bits = bit_buffer.read(len(bit_buffer))

        return from_bits(bits, endianness=endianness)
