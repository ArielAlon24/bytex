from dataclasses import dataclass

from structure.bits import BitBuffer, Bits, to_bits, from_bits
from structure.codecs.base_codec import BaseCodec
from structure.errors import ValidationError


@dataclass(frozen=True)
class DataCodec(BaseCodec[bytes]):
    def validate(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(bytes)}'"
            )

    def serialize(self, value: bytes) -> Bits:
        return to_bits(value)

    def deserialize(self, bit_buffer: BitBuffer) -> bytes:
        bits = bit_buffer.read(len(bit_buffer))

        return from_bits(bits)

    def __repr__(self) -> str:
        return f"Flag"
