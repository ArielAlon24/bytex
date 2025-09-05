from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError
from bytex.sign import Sign

U8_CODEC = IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)


@dataclass(frozen=True)
class PrefixBytesCodec(BaseCodec[bytes]):
    prefix_codec: IntegerCodec

    def serialize(self, value: bytes, endianness: Endianness) -> Bits:
        length = len(value)

        self.prefix_codec.validate(length)
        bits = self.prefix_codec.serialize(length, endianness=endianness)

        for num in value:
            bits += U8_CODEC.serialize(num, endianness=endianness)

        return bits

    def deserialize(self, bit_buffer: BitBuffer, endianness: Endianness) -> bytes:
        length = self.prefix_codec.deserialize(bit_buffer, endianness=endianness)

        return from_bits(bit_buffer.read(8 * length), endianness=Endianness.BIG)

    def validate(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )
