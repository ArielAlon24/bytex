from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class TerminatedListCodec(BaseCodec[Sequence[T]], Generic[T]):
    item_codec: BaseCodec[T]
    terminator: Bits

    def serialize(self, value: Sequence[T], endianness: Endianness) -> Bits:
        self.validate(value)

        bits = []

        for item in value:
            bits.extend(self.item_codec.serialize(item, endianness=endianness))

        bits.extend(self.terminator)

        return bits

    def deserialize(self, bit_buffer: BitBuffer, endianness: Endianness) -> Sequence[T]:
        items = []

        while True:
            peeked_data = bit_buffer.peek(len(self.terminator))
            if peeked_data == self.terminator:
                bit_buffer.read(len(self.terminator))
                break

            items.append(self.item_codec.deserialize(bit_buffer, endianness=endianness))

        return items

    def validate(self, value: Sequence[T]) -> None:
        if not isinstance(value, Sequence):
            raise ValidationError(
                f"{self.__class__.__name__} expects a sequence of items."
            )
