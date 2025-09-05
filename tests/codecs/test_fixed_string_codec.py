from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.fixed.fixed_string_codec import FixedStringCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError


@pytest.mark.parametrize("value, length", [("A", 1), ("ab", 2), ("01", 3)])
def test_fixed_string_validate_success(value: str, length: int) -> None:
    codec = FixedStringCodec(length=length)
    codec.validate(value)


@pytest.mark.parametrize("value, length", [("AB", 1), ("abcd", 3), (b"A", 1), (123, 1)])
def test_fixed_string_validate_failure(value: Any, length: int) -> None:
    codec = FixedStringCodec(length=length)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, length, expected",
    [
        ("A", 2, string_to_bits("0100000100000000")),
        ("ab", 3, string_to_bits("011000010110001000000000")),
        ("01", 2, string_to_bits("0011000000110001")),
    ],
)
def test_fixed_string_serialize(value: str, length: int, expected: Bits) -> None:
    codec = FixedStringCodec(length=length)
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        assert codec.serialize(value, endianness=endianness) == expected


@pytest.mark.parametrize(
    "length, bits, expected",
    [
        (2, string_to_bits("0100000100000000"), "A\x00"),
        (3, string_to_bits("011000010110001000000000"), "ab\x00"),
        (2, string_to_bits("0011000000110001"), "01"),
    ],
)
def test_fixed_string_deserialize(length: int, bits: Bits, expected: str) -> None:
    codec = FixedStringCodec(length=length)
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == expected


@pytest.mark.parametrize("value, length", [("A", 2), ("ab", 3), ("01", 2), ("xyz", 5)])
def test_fixed_string_roundtrip(value: str, length: int) -> None:
    codec = FixedStringCodec(length=length)

    for endianness in (Endianness.BIG, Endianness.LITTLE):
        bits = codec.serialize(value, endianness=endianness)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        padded = value + "\0" * (length - len(value))
        assert result == padded
