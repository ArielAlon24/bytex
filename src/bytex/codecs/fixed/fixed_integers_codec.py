from dataclasses import dataclass
from typing import Annotated, List

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.base_list_codec import BaseListCodec
from bytex.codecs.basic.char_codec import CharCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError

CHAR_CODEC = CharCodec()


@dataclass(frozen=True)
class FixedIntegersCodec(BaseListCodec[List[Annotated[int, IntegerCodec]]]):
    integer_codec: IntegerCodec
    length: int

    def get_inner_codec(self) -> BaseCodec:
        return self.integer_codec

    def serialize(
        self, value: List[Annotated[int, IntegerCodec]], endianes: Endianes
    ) -> Bits:
        bits = []

        for integer in value:
            bits += self.integer_codec.serialize(integer, endianes=endianes)

        for _ in range(self.length - len(value)):
            bits += self.integer_codec.serialize(0, endianes=endianes)

        return bits

    def deserialize(
        self, bit_buffer: BitBuffer, endianes: Endianes
    ) -> List[Annotated[int, IntegerCodec]]:
        return [
            self.integer_codec.deserialize(bit_buffer, endianes=endianes)
            for _ in range(self.length)
        ]

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
