from dataclasses import dataclass
from typing import Type

from structure._structure._structure import _Structure
from structure.bit_buffer import BitBuffer, Bits
from structure.codecs.base_codec import BaseCodec


@dataclass(frozen=True)
class StructureCodec(BaseCodec[_Structure]):
    structure_class: Type[_Structure]

    def serialize(self, value: _Structure) -> Bits:
        return value.dump_bits()

    def deserialize(self, bit_buffer: BitBuffer) -> _Structure:
        return self.structure_class.parse_bits(bit_buffer)

    def validate(self, value: _Structure) -> None:
        value.validate()

    def bit_remainder(self) -> int:
        return self.structure_class.bit_remainder()

    def __repr__(self) -> str:
        return "Structure"
