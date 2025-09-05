from __future__ import annotations

from typing import Any

from typing_extensions import Self

from bytex.bits import BitBuffer, Bits
from bytex.endianness import Endianness


class _Structure:
    def __init__(self, **data: Any) -> None:
        raise NotImplementedError

    def dump(self, endianness: Endianness = Endianness.LITTLE) -> bytes:
        raise NotImplementedError

    def dump_bits(self, endianness: Endianness = Endianness.LITTLE) -> Bits:
        raise NotImplementedError

    @classmethod
    def parse(
        cls,
        data: bytes,
        endianness: Endianness = Endianness.LITTLE,
        strict: bool = False,
    ) -> Self:
        raise NotImplementedError

    @classmethod
    def parse_bits(
        cls, buffer: BitBuffer, endianness: Endianness, strict: bool = False
    ) -> Self:
        raise NotImplementedError

    def validate(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
