from dataclasses import dataclass
from typing import Generic, List, TypeVar, Sequence

from structure.bits import BitBuffer, Bits
from structure.codecs.base_codec import BaseCodec
from structure.errors import ValidationError

T = TypeVar("T")


@dataclass(frozen=True)
class BitsTerminatedSequenceCodec(BaseCodec[Sequence[T]], Generic[T]):
    item_codec: BaseCodec[T]
    terminator: Bits

    def serialize(self, value: Sequence[T]) -> Bits:
        self.validate(value)

        bits: Bits = []

        for item in value:
            bits.extend(self.item_codec.serialize(item))

        bits.extend(self.terminator)

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> List[T]:
        result: List[T] = []
        recent_bits: Bits = []
        terminator_len = len(self.terminator)

        buffer_snapshot = BitBuffer()
        buffer_snapshot.write(bit_buffer.to_bits())

        while len(buffer_snapshot) >= terminator_len:
            item = self.item_codec.deserialize(buffer_snapshot)
            item_bits = self.item_codec.serialize(item)

            recent_bits.extend(item_bits)
            if len(recent_bits) > terminator_len:
                # Trim from the front
                recent_bits = recent_bits[-(terminator_len + len(item_bits)) :]

            result.append(item)

            if recent_bits[-terminator_len:] == self.terminator:
                return result[:-1] if len(self.terminator) > 0 else result

        raise ValidationError("Terminator not found before buffer ended.")

    def validate(self, value: Sequence[T]) -> None:
        if not isinstance(value, Sequence):
            raise ValidationError(
                f"{self.__class__.__name__} expects a sequence of items."
            )

    def bit_remainder(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f"TerminatedSequence(terminator=<{len(self.terminator)} bits>, item_codec={self.item_codec})"
