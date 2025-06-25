from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.char_codec import CharCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.errors import ValidationError


CHAR_CODEC = CharCodec()


@dataclass(frozen=True)
class PrefixStringCodec(BaseCodec[str]):
    prefix_codec: IntegerCodec

    def serialize(self, value: str) -> Bits:
        bits = []
        length = len(value)

        self.prefix_codec.validate(length)
        bits += self.prefix_codec.serialize(length)

        for char in value:
            bits += CHAR_CODEC.serialize(char)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> str:
        length = self.prefix_codec.deserialize(bit_buffer)

        return from_bits(bit_buffer.read(8 * length)).decode()

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )
