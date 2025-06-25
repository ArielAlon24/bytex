from dataclasses import dataclass
from typing import Annotated, List

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.char_codec import CharCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.errors import ValidationError


CHAR_CODEC = CharCodec()


@dataclass(frozen=True)
class FixedIntegersCodec(BaseCodec[List[Annotated[int, IntegerCodec]]]):
    integer_codec: IntegerCodec
    length: int

    def serialize(self, value: List[Annotated[int, IntegerCodec]]) -> Bits:
        bits = []

        for integer in value:
            bits += self.integer_codec.serialize(integer)

        for _ in range(self.length - len(value)):
            bits += self.integer_codec.serialize(0)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> List[Annotated[int, IntegerCodec]]:
        return [self.integer_codec.deserialize(bit_buffer) for _ in range(self.length)]

    def validate(self, value: List[Annotated[int, IntegerCodec]]) -> None:
        if not isinstance(value, list) or (
            len(value) and not isinstance(value[0], int)
        ):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type 'List[Annotated[int, IntegerCodec]]'"
            )

        if len(value) > self.length:
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must include up to `length` - {self.length} items"
            )
