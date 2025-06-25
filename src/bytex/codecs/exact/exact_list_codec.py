from dataclasses import dataclass
from typing import Generic, TypeVar, Sequence

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.errors import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class ExactListCodec(BaseCodec[Sequence[T]], Generic[T]):
    item_codec: BaseCodec[T]
    length: int

    def serialize(self, value: Sequence[T]) -> Bits:
        self.validate(value)

        bits = []

        for item in value:
            bits.extend(self.item_codec.serialize(item))

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> Sequence[T]:
        return [self.item_codec.deserialize(bit_buffer) for _ in range(self.length)]

    def validate(self, value: Sequence[T]) -> None:
        if not isinstance(value, Sequence):
            raise ValidationError(
                f"{self.__class__.__name__} expects a sequence of items."
            )

        if len(value) != self.length:
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of length `length` - {self.length} items"
            )
