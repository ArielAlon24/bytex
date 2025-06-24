from dataclasses import dataclass

from structure.bits import BitBuffer, Bits, from_bits
from structure.codecs.base_codec import BaseCodec
from structure.codecs.integer_codec import IntegerCodec
from structure.errors import ValidationError
from structure.sign import Sign


U8_CODEC = IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)


@dataclass(frozen=True)
class PrefixBytesCodec(BaseCodec[bytes]):
    integer_codec: IntegerCodec

    def serialize(self, value: bytes) -> Bits:
        bits = []
        length = len(value)

        self.integer_codec.validate(length)
        bits += self.integer_codec.serialize(length)

        for num in value:
            bits += U8_CODEC.serialize(num)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> bytes:
        length = self.integer_codec.deserialize(bit_buffer)

        return from_bits(bit_buffer.read(8 * length))

    def validate(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{bytes(str)}'"
            )

    def __repr__(self) -> str:
        return f"PrefixBytes({self.integer_codec})"
