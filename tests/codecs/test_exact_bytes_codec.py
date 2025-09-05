from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.exact.exact_bytes_codec import ExactBytesCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError


@pytest.mark.parametrize("value, length", [(b"A", 1), (b"ab", 2), (b"\x00\xff", 2)])
def test_exact_bytes_validate_success(value: bytes, length: int) -> None:
    codec = ExactBytesCodec(length=length)
    codec.validate(value)


@pytest.mark.parametrize("value, length", [(b"abc", 2), ("A", 1), (123, 1)])
def test_exact_bytes_validate_failure(value: Any, length: int) -> None:
    codec = ExactBytesCodec(length=length)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, length, expected",
    [
        (b"A", 1, string_to_bits("01000001")),
        (b"ab", 2, string_to_bits("0110000101100010")),
        (b"\x00\xff", 2, string_to_bits("0000000011111111")),
    ],
)
def test_exact_bytes_serialize(value: bytes, length: int, expected: Bits) -> None:
    codec = ExactBytesCodec(length=length)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        assert codec.serialize(value, endianes=endianes) == expected


@pytest.mark.parametrize(
    "length, bits, expected",
    [
        (1, string_to_bits("01000001"), b"A"),
        (2, string_to_bits("0110000101100010"), b"ab"),
        (2, string_to_bits("0000000011111111"), b"\x00\xff"),
    ],
)
def test_exact_bytes_deserialize(length: int, bits: Bits, expected: bytes) -> None:
    codec = ExactBytesCodec(length=length)

    for endianes in (Endianes.BIG, Endianes.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == expected


@pytest.mark.parametrize(
    "value, length", [(b"A", 1), (b"ab", 2), (b"\x00\xff", 2), (b"xyz", 3)]
)
def test_exact_bytes_roundtrip(value: bytes, length: int) -> None:
    codec = ExactBytesCodec(length=length)

    for endianes in (Endianes.BIG, Endianes.LITTLE):
        bits: Bits = codec.serialize(value, endianes=endianes)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == value
