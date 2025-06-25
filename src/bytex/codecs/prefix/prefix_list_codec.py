from dataclasses import dataclass
from typing import Generic, TypeVar, Sequence

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.errors import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class PrefixListCodec(BaseCodec[Sequence[T]], Generic[T]):
    prefix_codec: IntegerCodec
    item_codec: BaseCodec[T]

    def serialize(self, value: Sequence[T]) -> Bits:
        bits = []
        length = len(value)

        self.prefix_codec.validate(length)
        bits += self.prefix_codec.serialize(length)

        for num in value:
            bits += self.item_codec.serialize(num)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> Sequence[T]:
        length = self.prefix_codec.deserialize(bit_buffer)
        return [self.item_codec.deserialize(bit_buffer) for _ in range(length)]

    def validate(self, value: Sequence[T]) -> None:
        if not isinstance(value, Sequence):
            raise ValidationError(
                f"{self.__class__.__name__} expects a sequence of items."
            )
