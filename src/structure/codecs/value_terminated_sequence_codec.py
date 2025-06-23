from dataclasses import dataclass
from typing import Generic, List, TypeVar, Sequence

from structure.bits import BitBuffer, Bits
from structure.codecs.base_codec import BaseCodec
from structure.errors import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class ValueTerminatedSequenceCodec(BaseCodec[Sequence[T]], Generic[T]):
    item_codec: BaseCodec[T]
    terminator: Sequence[T]

    def serialize(self, value: Sequence[T]) -> Bits:
        self.validate(value)

        bits = []

        for item in value:
            bits += self.item_codec.serialize(item)

        for terminator_item in self.terminator:
            bits += self.item_codec.serialize(terminator_item)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> List[T]:
        result: List[T] = []
        recent: List[T] = []

        terminator_len = len(self.terminator)

        while True:
            item = self.item_codec.deserialize(bit_buffer)
            result.append(item)
            recent.append(item)

            if len(recent) > terminator_len:
                recent.pop(0)

            if recent == list(self.terminator):
                return result[:-terminator_len]

    def validate(self, value: Sequence[T]) -> None:
        if not isinstance(value, Sequence):
            raise ValidationError(f"{self.__class__.__name__} expects a list of items.")

        if self._contains_terminator(value):
            raise ValidationError(
                f"Input sequence must not contain the terminator sequence {self.terminator}"
            )

    def _contains_terminator(self, value: Sequence[T]) -> bool:
        term_len = len(self.terminator)
        if term_len == 0:
            return False

        for i in range(len(value) - term_len + 1):
            if value[i : i + term_len] == list(self.terminator):
                return True
        return False

    def bit_remainder(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f"TerminatedSequence(terminator={self.terminator}, item_codec={self.item_codec})"
