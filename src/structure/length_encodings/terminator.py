from typing import Union
from dataclasses import dataclass

from structure.length_encodings.base_length_encoding import BaseLengthEncoding
from structure.bits import Bits, to_bits


@dataclass
class Terminator(BaseLengthEncoding):
    value: Union[str, bytes, Bits]

    def get_terminator(self) -> Bits:
        if isinstance(self.value, str) or isinstance(self.value, bytes):
            return to_bits(self.value)

        return self.value
