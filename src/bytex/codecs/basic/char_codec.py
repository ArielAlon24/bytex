from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError
from bytex.sign import Sign

U8_CODEC = IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)


@dataclass(frozen=True)
class CharCodec(BaseCodec[str]):
    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )

        if len(value) != 1:
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s must be of length 1"
            )

        return U8_CODEC.validate(ord(value))

    def serialize(self, value: str, endianness: Endianness) -> Bits:
        return U8_CODEC.serialize(ord(value), endianness=endianness)

    def deserialize(self, bit_buffer: BitBuffer, endianness: Endianness) -> str:
        return chr(U8_CODEC.deserialize(bit_buffer, endianness=endianness))
