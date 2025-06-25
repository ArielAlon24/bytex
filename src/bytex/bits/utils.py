from typing import Union

from bytex.bits.types import Bits
from bytex.errors import ValidationError


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


def to_binary(bits: Bits) -> str:
    """
    Converts a list of bits (booleans) into a hexdump-like binary string.

    Each line represents 8 bytes (64 bits), formatted as:
        <byte_offset_hex>  <8 binary byte groups>

    Only full bytes (8 bits) are included. Incomplete trailing bits are ignored.
    """
    if not bits:
        return ""

    lines = []
    bytes_per_line = 8
    total_bytes = len(bits) // 8

    for line_index in range(0, total_bytes, bytes_per_line):
        line_bits = bits[line_index * 8 : (line_index + bytes_per_line) * 8]
        byte_strs = []

        for i in range(0, len(line_bits), 8):
            byte = line_bits[i : i + 8]
            byte_str = "".join("1" if bit else "0" for bit in byte)
            byte_strs.append(byte_str)

        address = f"{line_index:08x}"
        line = f"{address}  {' '.join(byte_strs)}"
        lines.append(line)

    return "\n".join(lines)


def is_subsequence(sub: Bits, full: Bits) -> bool:
    n, m = len(full), len(sub)
    if m == 0:
        return True

    for i in range(n - m + 1):
        if full[i : i + m] == sub:
            return True
    return False
