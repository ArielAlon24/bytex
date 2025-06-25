from dataclasses import dataclass

from bytex.bits import BitBuffer, Bits
from bytex.codecs.base_codec import BaseCodec
from bytex.sign import Sign
from bytex.errors import ValidationError


@dataclass(frozen=True)
class IntegerCodec(BaseCodec[int]):
    bit_count: int
    sign: Sign

    def __post_init__(self) -> None:
        if self.bit_count <= 0:
            raise ValidationError(
                "Invalid `bit_count`, `bit_count` should be a positive number"
            )

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(int)}'"
            )

        if self.sign == Sign.SIGNED:
            minimum = -(1 << (self.bit_count - 1))
            maximum = (1 << (self.bit_count - 1)) - 1
        else:
            minimum = 0
            maximum = (1 << self.bit_count) - 1

        if not (minimum <= value <= maximum):
            raise ValidationError(
                f"Value {value} does not fit in "
                f"a {repr(self)} integer "
                f"range [{minimum}, {maximum}]"
            )

    def serialize(self, value: int) -> Bits:
        bits = []

        if self.sign == Sign.SIGNED and value < 0:
            value = (1 << self.bit_count) + value

        for i in reversed(range(self.bit_count)):
            bits.append(bool((value >> i) & 1))

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> int:
        bits = bit_buffer.read(self.bit_count)

        value = 0
        for bit in bits:
            value = (value << 1) | int(bit)

        if self.sign == Sign.SIGNED:
            sign_bit = 1 << (self.bit_count - 1)
            if value & sign_bit:
                value -= 1 << self.bit_count

        return value
