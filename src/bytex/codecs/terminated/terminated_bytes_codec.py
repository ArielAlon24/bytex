from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.bits.utils import is_subsequence, to_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.errors import ValidationError
from bytex.sign import Sign


U8_CODEC = IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)


@dataclass(frozen=True)
class TerminatedBytesCodec(BaseCodec[bytes]):
    terminator: Bits

    def serialize(self, value: bytes) -> Bits:
        bits = []

        for char in value:
            bits += U8_CODEC.serialize(char)

        bits += self.terminator

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> bytes:
        result = bytearray()

        while True:
            peek_data = bit_buffer.peek(len(self.terminator))
            if peek_data == self.terminator:
                bit_buffer.read(len(self.terminator))
                break

            result.append(U8_CODEC.deserialize(bit_buffer))

        return bytes(result)

    def validate(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{bytes(bytes)}'"
            )

        bits = to_bits(value)

        if is_subsequence(self.terminator, bits):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value cannot contain it's own "
                f"terminator - {from_bits(self.terminator)}"
            )
