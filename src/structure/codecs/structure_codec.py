from dataclasses import dataclass
from typing import Type

from structure._structure._structure import _Structure
from structure.bits import BitBuffer, Bits
from structure.codecs.base_codec import BaseCodec
from structure.errors import ValidationError


@dataclass(frozen=True)
class StructureCodec(BaseCodec[_Structure]):
    structure_class: Type[_Structure]

    def serialize(self, value: _Structure) -> Bits:
        return value.dump_bits()

    def deserialize(self, bit_buffer: BitBuffer) -> _Structure:
        return self.structure_class.parse_bits(bit_buffer)

    def validate(self, value: _Structure) -> None:
        if not isinstance(value, _Structure):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be a 'Structure' as well"
            )

        value.validate()

    def __repr__(self) -> str:
        return "Structure"
