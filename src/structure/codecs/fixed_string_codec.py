from dataclasses import dataclass

from structure.bits import BitBuffer, Bits, from_bits
from structure.codecs.base_codec import BaseCodec
from structure.codecs.char_codec import CharCodec
from structure.errors import ValidationError


CHAR_CODEC = CharCodec()
EMPTY_CHAR = CHAR_CODEC.serialize("\0")


@dataclass(frozen=True)
class FixedStringCodec(BaseCodec[str]):
    length: int

    def serialize(self, value: str) -> Bits:
        bits = []

        for char in value:
            bits += CHAR_CODEC.serialize(char)

        for _ in range(self.length - len(value)):
            bits += EMPTY_CHAR

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> str:
        return from_bits(bit_buffer.read(8 * self.length)).decode()

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )

        if len(value) > self.length:
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be up to `length` ({self.length}) characters"
            )

    def bit_remainder(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f"FixedString({self.length})"
