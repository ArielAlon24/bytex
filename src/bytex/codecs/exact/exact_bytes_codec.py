from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.errors import ValidationError
from bytex.sign import Sign


U8_CODEC = IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)
EMPTY_BYTE = U8_CODEC.serialize(0)


@dataclass(frozen=True)
class ExactBytesCodec(BaseCodec[bytes]):
    length: int

    def serialize(self, value: bytes) -> Bits:
        bits = []

        for char in value:
            bits += U8_CODEC.serialize(char)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> bytes:
        return from_bits(bit_buffer.read(U8_CODEC.bit_count * self.length))

    def validate(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{bytes(bytes)}'"
            )

        if len(value) != self.length:
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of length `length` - {self.length} characters"
            )
