from dataclasses import dataclass

from bytex import endianes
from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.errors import ValidationError


@dataclass(frozen=True)
class FlagCodec(BaseCodec[bool]):
    def validate(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(bool)}'"
            )

    def serialize(self, value: bool, endianes: endianes.Endianes) -> Bits:
        return [value]

    def deserialize(self, bit_buffer: BitBuffer, endianes: endianes.Endianes) -> bool:
        return bit_buffer.read(1)[0]
