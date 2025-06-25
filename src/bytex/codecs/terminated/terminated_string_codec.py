from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.bits.utils import is_subsequence, to_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.char_codec import CharCodec
from bytex.errors import ValidationError


CHAR_CODEC = CharCodec()


@dataclass(frozen=True)
class TerminatedStringCodec(BaseCodec[str]):
    terminator: Bits

    def serialize(self, value: str) -> Bits:
        bits = []

        for char in value:
            bits += CHAR_CODEC.serialize(char)

        bits += self.terminator

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> str:
        result = str()

        while True:
            peek_data = bit_buffer.peek(len(self.terminator))
            if peek_data == self.terminator:
                bit_buffer.read(len(self.terminator))
                break

            result += CHAR_CODEC.deserialize(bit_buffer)

        return result

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )

        bits = to_bits(value)

        if is_subsequence(self.terminator, bits):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value cannot contain it's own "
                f"terminator - {from_bits(self.terminator)}"
            )
