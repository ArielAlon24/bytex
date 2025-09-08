from functools import lru_cache
from typing import Annotated

from bytex.bits import to_bits
from bytex.codecs import (
    CharCodec,
    DataCodec,
    FlagCodec,
    IntegerCodec,
    TerminatedBytesCodec,
    TerminatedStringCodec,
)
from bytex.sign import Sign


@lru_cache
def _UInt(bits: int):
    return Annotated[int, IntegerCodec(bit_count=bits, sign=Sign.UNSIGNED)]


@lru_cache
def _SInt(bits: int):
    return Annotated[int, IntegerCodec(bit_count=bits, sign=Sign.SIGNED)]


_types_byte_length = (1, 2, 3, 4, 8, 16, 32, 64, 128, 256)

for n in _types_byte_length:
    globals()[f"U{n}"] = _UInt(n)
    globals()[f"I{n}"] = _SInt(n)

Char = Annotated[str, CharCodec()]
Flag = Annotated[bool, FlagCodec()]
Data = Annotated[bytes, DataCodec()]
CStr = Annotated[str, TerminatedStringCodec(terminator=to_bits("\0"))]
ByteCStr = Annotated[bytes, TerminatedBytesCodec(terminator=to_bits(b"\x00"))]