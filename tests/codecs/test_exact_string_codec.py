from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.exact.exact_string_codec import ExactStringCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError


@pytest.mark.parametrize("value, length", [("A", 1), ("ab", 2), ("01", 2)])
def test_exact_string_validate_success(value: str, length: int) -> None:
    codec = ExactStringCodec(length=length)
    codec.validate(value)


@pytest.mark.parametrize("value, length", [("A", 2), ("abc", 2), (b"A", 1), (123, 1)])
def test_exact_string_validate_failure(value: Any, length: int) -> None:
    codec = ExactStringCodec(length=length)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, length, expected",
    [
        ("A", 1, string_to_bits("01000001")),
        ("ab", 2, string_to_bits("0110000101100010")),
        ("01", 2, string_to_bits("0011000000110001")),
    ],
)
def test_exact_string_serialize(value: str, length: int, expected: Bits) -> None:
    codec = ExactStringCodec(length=length)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        assert codec.serialize(value, endianes=endianes) == expected


@pytest.mark.parametrize(
    "length, bits, expected",
    [
        (1, string_to_bits("01000001"), "A"),
        (2, string_to_bits("0110000101100010"), "ab"),
        (2, string_to_bits("0011000000110001"), "01"),
    ],
)
def test_exact_string_deserialize(length: int, bits: Bits, expected: str) -> None:
    codec = ExactStringCodec(length=length)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == expected


@pytest.mark.parametrize("value, length", [("A", 1), ("ab", 2), ("01", 2), ("xyz", 3)])
def test_exact_string_roundtrip(value: str, length: int) -> None:
    codec = ExactStringCodec(length=length)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        bits = codec.serialize(value, endianes=endianes)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == value
