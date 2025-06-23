from dataclasses import dataclass
from structure.bits import BitBuffer, Bits, from_bits
from structure.codecs.base_codec import BaseCodec
from structure.codecs.char_codec import CharCodec
from structure.codecs.integer_codec import IntegerCodec
from structure.errors import InsufficientDataError, ValidationError
from structure.sign import Sign


CHAR_CODEC = CharCodec()


@dataclass(frozen=True)
class TerminatedStringCodec(BaseCodec[str]):
    terminator: Bits

    def serialize(self, value: str) -> Bits:
        bits = []

        for char in value:
            bits += CHAR_CODEC.serialize(char)

        bits += self.terminator

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> str:
        result = str()

        while True:
            peek_data = bit_buffer.peek(len(self.terminator))
            if peek_data == self.terminator:
                bit_buffer.read(len(self.terminator))
                break

            result += CHAR_CODEC.deserialize(bit_buffer)

        return result

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValidationError(
                f"Invalid value, a {self.__class__.__name__}'s value must be of type '{str(str)}'"
            )

    def bit_remainder(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f"TerminatedString({repr(from_bits(self.terminator))})"
