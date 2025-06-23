from typing import Union

from structure.bits.types import Bits
from structure.errors import ValidationError


def to_bits(data: Union[str, bytes]) -> Bits:
    if isinstance(data, str):
        data = data.encode()

    bits = []

    for byte in data:
        for i in range(8):
            bits.append(bool((byte >> (7 - i)) & 1))

    return bits


def from_bits(bits: Bits) -> bytes:
    if len(bits) % 8 != 0:
        raise ValidationError("Number of bits must be a multiple of 8")

    result = bytearray()

    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte |= (1 if bits[i + j] else 0) << (7 - j)
        result.append(byte)

    return bytes(result)
