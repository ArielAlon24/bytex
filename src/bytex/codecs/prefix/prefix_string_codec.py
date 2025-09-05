from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.char_codec import CharCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError

CHAR_CODEC = CharCodec()


@dataclass(frozen=True)
class PrefixStringCodec(BaseCodec[str]):
    prefix_codec: IntegerCodec

    def serialize(self, value: str, endianness: Endianness) -> Bits:
        length = len(value)

        self.prefix_codec.validate(length)
        bits = self.prefix_codec.serialize(length, endianness=endianness)

        for char in value:
            bits += CHAR_CODEC.serialize(char, endianness=endianness)

        return bits

    def deserialize(self, bit_buffer: BitBuffer, endianness: Endianness) -> str:
        length = self.prefix_codec.deserialize(bit_buffer, endianness=endianness)

        return from_bits(
            bit_buffer.read(8 * length), endianness=Endianness.BIG
        ).decode()

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )
