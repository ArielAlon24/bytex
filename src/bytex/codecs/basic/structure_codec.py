from dataclasses import dataclass
from typing import Type

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError
from bytex.structure._structure import _Structure


@dataclass(frozen=True)
class StructureCodec(BaseCodec[_Structure]):
    structure_class: Type[_Structure]

    def serialize(self, value: _Structure, endianness: Endianness) -> Bits:
        return value.dump_bits(endianness=endianness)

    def deserialize(self, bit_buffer: BitBuffer, endianness: Endianness) -> _Structure:
        return self.structure_class.parse_bits(bit_buffer, endianness=endianness)

    def validate(self, value: _Structure) -> None:
        if not isinstance(value, _Structure):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be a 'Structure' as well"
            )

        value.validate()
