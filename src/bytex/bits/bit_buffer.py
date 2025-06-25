from __future__ import annotations

from bytex.endianes import Endianes
from bytex.errors import AlignmentError, InsufficientDataError
from bytex.bits.types import Bits


class BitBuffer:
    def __init__(self) -> None:
        self._bits: Bits = []

    def write(self, bits: Bits) -> None:
        self._bits.extend(bits)

    def read(self, count: int) -> Bits:
        if count > len(self._bits):
            raise InsufficientDataError(
                f"Cannot read {count} bits, only {len(self._bits)} available"
            )
        result = self._bits[:count]
        self._bits = self._bits[count:]
        return result

    def peek(self, count: int) -> Bits:
        if count > len(self._bits):
            raise InsufficientDataError(
                f"Cannot read {count} bits, only {len(self._bits)} available"
            )

        return self._bits[:count]

    def to_bits(self) -> Bits:
        return self._bits

    def to_bytes(self, endianes: Endianes) -> bytes:
        if len(self._bits) % 8 != 0:
            raise AlignmentError(
                "Bit buffer is not aligned to full bytes (size is not divisible by 8)"
            )

        byte_count = len(self._bits) // 8
        byte_list = []

        for byte_index in range(byte_count):
            bits = self._bits[byte_index * 8 : (byte_index + 1) * 8]
            value = 0
            for i, bit in enumerate(bits):
                bit_position = 7 - i
                if bit:
                    value |= 1 << bit_position
            byte_list.append(value)

        if endianes == Endianes.LITTLE:
            byte_list.reverse()

        return bytes(byte_list)

    @classmethod
    def from_bytes(cls, data: bytes, endianes: Endianes) -> BitBuffer:
        buffer = cls()
        byte_list = list(data)
        if endianes == Endianes.LITTLE:
            byte_list.reverse()

        for byte in byte_list:
            for i in range(8):
                bit_position = 7 - i
                bit = (byte >> bit_position) & 1
                buffer._bits.append(bool(bit))

        return buffer

    def __len__(self) -> int:
        return len(self._bits)
