from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.fixed.fixed_bytes_codec import FixedBytesCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError


@pytest.mark.parametrize("value, length", [(b"A", 1), (b"ab", 2), (b"\x00\xff", 3)])
def test_fixed_bytes_validate_success(value: bytes, length: int) -> None:
    codec = FixedBytesCodec(length=length)
    codec.validate(value)


@pytest.mark.parametrize("value, length", [(b"ABC", 2), ("A", 1), (123, 1)])
def test_fixed_bytes_validate_failure(value: Any, length: int) -> None:
    codec = FixedBytesCodec(length=length)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, length, expected",
    [
        (b"A", 2, string_to_bits("0100000100000000")),
        (b"ab", 3, string_to_bits("011000010110001000000000")),
        (b"\x00\xff", 2, string_to_bits("0000000011111111")),
    ],
)
def test_fixed_bytes_serialize(value: bytes, length: int, expected: Bits) -> None:
    codec = FixedBytesCodec(length=length)
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        assert codec.serialize(value, endianness=endianness) == expected


@pytest.mark.parametrize(
    "length, bits, expected",
    [
        (2, string_to_bits("0100000100000000"), b"A\x00"),
        (3, string_to_bits("011000010110001000000000"), b"ab\x00"),
        (2, string_to_bits("0000000011111111"), b"\x00\xff"),
    ],
)
def test_fixed_bytes_deserialize(length: int, bits: Bits, expected: bytes) -> None:
    codec = FixedBytesCodec(length=length)
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == expected


@pytest.mark.parametrize(
    "value, length", [(b"A", 2), (b"ab", 3), (b"\x00\xff", 2), (b"xyz", 5)]
)
def test_fixed_bytes_roundtrip(value: bytes, length: int) -> None:
    codec = FixedBytesCodec(length=length)
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        bits: Bits = codec.serialize(value, endianness=endianness)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        padded = value + b"\x00" * (length - len(value))
        assert result == padded
