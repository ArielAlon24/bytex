from dataclasses import dataclass

from structure.bits import BitBuffer, Bits, from_bits
from structure.codecs.base_codec import BaseCodec
from structure.codecs.char_codec import CharCodec
from structure.codecs.integer_codec import IntegerCodec
from structure.errors import ValidationError


CHAR_CODEC = CharCodec()
EMPTY_CHAR = CHAR_CODEC.serialize("\0")


@dataclass(frozen=True)
class PrefixStringCodec(BaseCodec[str]):
    integer_codec: IntegerCodec

    def serialize(self, value: str) -> Bits:
        bits = []
        length = len(value)

        self.integer_codec.validate(length)
        bits += self.integer_codec.serialize(length)

        for char in value:
            bits += CHAR_CODEC.serialize(char)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> str:
        length = self.integer_codec.deserialize(bit_buffer)

        return from_bits(bit_buffer.read(8 * length)).decode()

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )

    def bit_remainder(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f"PrefixString({self.integer_codec})"
