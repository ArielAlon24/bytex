from __future__ import annotations

from typing import Any
from typing_extensions import Self
from bytex.endianes import Endianes
from bytex.bits import BitBuffer, Bits


class _Structure:
    def __init__(self, **data: Any) -> None:
        raise NotImplementedError

    def dump(self, endianes: Endianes = Endianes.LITTLE) -> bytes:
        raise NotImplementedError

    def dump_bits(self, endianes: Endianes = Endianes.LITTLE) -> Bits:
        raise NotImplementedError

    @classmethod
    def parse(
        cls, data: bytes, endianes: Endianes = Endianes.LITTLE, strict: bool = False
    ) -> Self:
        raise NotImplementedError

    @classmethod
    def parse_bits(cls, buffer: BitBuffer, strict: bool = False) -> Self:
        raise NotImplementedError

    def validate(self) -> None:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
