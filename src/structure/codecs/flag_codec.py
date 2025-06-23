from dataclasses import dataclass

from structure.bit_buffer import BitBuffer, Bits
from structure.codecs.base_codec import BaseCodec


@dataclass(frozen=True)
class FlagCodec(BaseCodec[bool]):
    def validate(self, value: bool) -> None:
        pass

    def serialize(self, value: bool) -> Bits:
        return [value]

    def deserialize(self, bit_buffer: BitBuffer) -> bool:
        return bit_buffer.read(1)[0]

    def bit_remainder(self) -> int:
        return 1

    def __repr__(self) -> str:
        return f"Flag"
