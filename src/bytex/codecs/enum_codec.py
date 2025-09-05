from dataclasses import dataclass
from typing import Type

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.endianness import Endianness
from bytex.errors import ParsingError, ValidationError
from bytex.structure_enum import _StructureEnum


@dataclass(frozen=True)
class EnumCodec(BaseCodec[_StructureEnum]):
    enum: Type[_StructureEnum]
    item_codec: BaseCodec

    def validate(self, value: _StructureEnum) -> None:
        if not isinstance(value, self.enum):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(_StructureEnum)}'"
            )

    def serialize(self, value: _StructureEnum, endianness: Endianness) -> Bits:
        return self.item_codec.serialize(value.value, endianness=endianness)

    def deserialize(
        self, bit_buffer: BitBuffer, endianness: Endianness
    ) -> _StructureEnum:
        value = self.item_codec.deserialize(bit_buffer, endianness=endianness)

        try:
            return self.enum(value)
        except ValueError as e:
            raise ParsingError(
                f"Failed to parse a '{self.enum.__name__}' item - unknown value '{value}'"
            ) from e
