from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.base_list_codec import BaseListCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class PrefixListCodec(BaseListCodec[Sequence[T]], Generic[T]):
    prefix_codec: IntegerCodec
    item_codec: BaseCodec[T]

    def get_inner_codec(self) -> BaseCodec:
        return self.item_codec

    def serialize(self, value: Sequence[T], endianes: Endianes) -> Bits:
        length = len(value)

        self.prefix_codec.validate(length)
        bits = self.prefix_codec.serialize(length, endianes=endianes)

        for num in value:
            bits += self.item_codec.serialize(num, endianes=endianes)

        return bits

    def deserialize(self, bit_buffer: BitBuffer, endianes: Endianes) -> Sequence[T]:
        length = self.prefix_codec.deserialize(bit_buffer, endianes=endianes)
        return [
            self.item_codec.deserialize(bit_buffer, endianes=endianes)
            for _ in range(length)
        ]

    def validate(self, value: Sequence[T]) -> None:
        if not isinstance(value, Sequence):
            raise ValidationError(
                f"{self.__class__.__name__} expects a sequence of items."
            )
