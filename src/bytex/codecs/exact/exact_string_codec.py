from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.char_codec import CharCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError

CHAR_CODEC = CharCodec()
EMPTY_CHAR = CHAR_CODEC.serialize("\0", endianes=Endianes.BIG)


@dataclass(frozen=True)
class ExactStringCodec(BaseCodec[str]):
    length: int

    def serialize(self, value: str, endianes: Endianes) -> Bits:
        bits = []

        for char in value:
            bits += CHAR_CODEC.serialize(char, endianes=endianes)

        return bits

    def deserialize(self, bit_buffer: BitBuffer, endianes: Endianes) -> str:
        return from_bits(
            bit_buffer.read(8 * self.length), endianes=Endianes.BIG
        ).decode()

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )

        if len(value) != self.length:
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of length `length` - {self.length} characters"
            )
