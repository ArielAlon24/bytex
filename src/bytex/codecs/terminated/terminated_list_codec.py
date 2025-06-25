from dataclasses import dataclass
from typing import Generic, TypeVar, Sequence

from bytex.bits import BitBuffer, Bits, from_bits
from bytex.codecs.base_codec import BaseCodec
from bytex.errors import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class TerminatedListCodec(BaseCodec[Sequence[T]], Generic[T]):
    item_codec: BaseCodec[T]
    terminator: Bits

    def serialize(self, value: Sequence[T]) -> Bits:
        self.validate(value)

        bits: Bits = []

        for item in value:
            bits.extend(self.item_codec.serialize(item))

        bits.extend(self.terminator)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> Sequence[T]:
        items = []

        while True:
            peeked_data = bit_buffer.peek(len(self.terminator))
            if peeked_data == self.terminator:
                bit_buffer.read(len(self.terminator))
                break

            items.append(self.item_codec.deserialize(bit_buffer))

        return items

    def validate(self, value: Sequence[T]) -> None:
        if not isinstance(value, Sequence):
            raise ValidationError(
                f"{self.__class__.__name__} expects a sequence of items."
            )
