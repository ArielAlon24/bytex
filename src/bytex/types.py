from typing import Annotated

from bytex.bits import to_bits
from bytex.sign import Sign
from bytex.codecs import (
    IntegerCodec,
    FlagCodec,
    TerminatedBytesCodec,
    TerminatedStringCodec,
    CharCodec,
    DataCodec,
)


U1 = Annotated[int, IntegerCodec(bit_count=1, sign=Sign.UNSIGNED)]
U3 = Annotated[int, IntegerCodec(bit_count=3, sign=Sign.UNSIGNED)]
U2 = Annotated[int, IntegerCodec(bit_count=2, sign=Sign.UNSIGNED)]
U4 = Annotated[int, IntegerCodec(bit_count=4, sign=Sign.UNSIGNED)]
U8 = Annotated[int, IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)]
U16 = Annotated[int, IntegerCodec(bit_count=16, sign=Sign.UNSIGNED)]
U32 = Annotated[int, IntegerCodec(bit_count=32, sign=Sign.UNSIGNED)]
U64 = Annotated[int, IntegerCodec(bit_count=64, sign=Sign.UNSIGNED)]
U128 = Annotated[int, IntegerCodec(bit_count=128, sign=Sign.UNSIGNED)]
U256 = Annotated[int, IntegerCodec(bit_count=256, sign=Sign.UNSIGNED)]

I1 = Annotated[int, IntegerCodec(bit_count=1, sign=Sign.SIGNED)]
I2 = Annotated[int, IntegerCodec(bit_count=2, sign=Sign.SIGNED)]
I3 = Annotated[int, IntegerCodec(bit_count=3, sign=Sign.SIGNED)]
I4 = Annotated[int, IntegerCodec(bit_count=4, sign=Sign.SIGNED)]
I8 = Annotated[int, IntegerCodec(bit_count=8, sign=Sign.SIGNED)]
I16 = Annotated[int, IntegerCodec(bit_count=16, sign=Sign.SIGNED)]
I32 = Annotated[int, IntegerCodec(bit_count=32, sign=Sign.SIGNED)]
I64 = Annotated[int, IntegerCodec(bit_count=64, sign=Sign.SIGNED)]
I128 = Annotated[int, IntegerCodec(bit_count=128, sign=Sign.SIGNED)]
I256 = Annotated[int, IntegerCodec(bit_count=256, sign=Sign.SIGNED)]

Char = Annotated[str, CharCodec()]
Flag = Annotated[bool, FlagCodec()]
Data = Annotated[bytes, DataCodec()]
CStr = Annotated[str, TerminatedStringCodec(terminator=to_bits("\0"))]
ByteCStr = Annotated[bytes, TerminatedBytesCodec(terminator=to_bits(b"\x00"))]
