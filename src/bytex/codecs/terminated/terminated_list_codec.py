from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class TerminatedListCodec(BaseCodec[Sequence[T]], Generic[T]):
    item_codec: BaseCodec[T]
    terminator: Bits

    def serialize(self, value: Sequence[T], endianes: Endianes) -> Bits:
        self.validate(value)

        bits = []

        for item in value:
            bits.extend(self.item_codec.serialize(item, endianes=endianes))

        bits.extend(self.terminator)

        return bits

    def deserialize(self, bit_buffer: BitBuffer, endianes: Endianes) -> Sequence[T]:
        items = []

        while True:
            peeked_data = bit_buffer.peek(len(self.terminator))
            if peeked_data == self.terminator:
                bit_buffer.read(len(self.terminator))
                break

            items.append(self.item_codec.deserialize(bit_buffer, endianes=endianes))

        return items

    def validate(self, value: Sequence[T]) -> None:
        if not isinstance(value, Sequence):
            raise ValidationError(
                f"{self.__class__.__name__} expects a sequence of items."
            )
