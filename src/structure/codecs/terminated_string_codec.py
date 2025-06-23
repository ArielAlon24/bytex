from dataclasses import dataclass
from structure.bit_buffer import BitBuffer, Bits
from structure.codecs.base_codec import BaseCodec
from structure.codecs.integer_codec import IntegerCodec
from structure.sign import Sign


CHAR_CODEC: IntegerCodec = IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)


@dataclass(frozen=True)
class TerminatedStringCodec(BaseCodec[str]):
    terminator: str

    def serialize(self, value: str) -> Bits:
        bits = []

        for char in value:
            bits += CHAR_CODEC.serialize(ord(char))

        for term_char in self.terminator:
            bits += CHAR_CODEC.serialize(ord(term_char))

        return bits

    def deserialize(self, bit_buffer: BitBuffer) -> str:
        buffer = []
        recent = []

        terminator_ord = list(map(ord, self.terminator))
        terminator_length = len(terminator_ord)

        while True:
            char = CHAR_CODEC.deserialize(bit_buffer)
            buffer.append(char)
            recent.append(char)

            if len(recent) > terminator_length:
                recent.pop(0)

            if recent == terminator_ord:
                return "".join(map(chr, buffer[:-terminator_length]))

    def validate(self, value: str) -> None:
        if self.terminator in value:
            raise ValueError(
                f"Input string must not contain the terminator sequence {repr(self.terminator)}"
            )

    def bit_remainder(self) -> int:
        return 0

    def __repr__(self) -> str:
        return f"TerminatedString({repr(self.terminator)})"
