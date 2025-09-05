from __future__ import annotations

from typing import List

from bytex.bits.utils import from_bits, to_bits
from bytex.errors import InsufficientDataError

Bits = List[bool]


class BitBuffer:
    def __init__(self) -> None:
        self._bits: Bits = []

    def write(self, bits: Bits) -> None:
        if len(bits) < 8:
            self._bits.extend(bits)
        else:
            for i in range(0, len(bits), 8):
                chunk = bits[i : i + 8]
                self._bits.extend(chunk)

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
                f"Cannot peek {count} bits, only {len(self._bits)} available"
            )

        return self._bits[:count]

    def to_bits(self) -> Bits:
        return list(self._bits)

    def to_bytes(self) -> bytes:
        return from_bits(self._bits)

    @classmethod
    def from_bytes(cls, data: bytes) -> BitBuffer:
        bit_buffer = cls()
        bits = to_bits(data)
        bit_buffer.write(bits)

        return bit_buffer

    def __len__(self) -> int:
        return len(self._bits)
