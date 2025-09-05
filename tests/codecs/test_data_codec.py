from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.basic.data_codec import DataCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError


@pytest.mark.parametrize("value", [b"", b"A", b"hello", bytes(range(5))])
def test_data_validate_success(value: bytes) -> None:
    codec = DataCodec()
    codec.validate(value)


@pytest.mark.parametrize("value", [None, "A", 123, True, ["a"], {"k": b"v"}])
def test_data_validate_failure(value: Any) -> None:
    codec = DataCodec()
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, expected_big, expected_little",
    [
        (b"A", string_to_bits("01000001"), string_to_bits("01000001")),
        (b"ab", string_to_bits("0110000101100010"), string_to_bits("0110001001100001")),
        (
            b"\x00\xff",
            string_to_bits("0000000011111111"),
            string_to_bits("1111111100000000"),
        ),
    ],
)
def test_data_serialize(
    value: bytes, expected_big: Bits, expected_little: Bits
) -> None:
    codec = DataCodec()
    assert codec.serialize(value, endianes=Endianes.BIG) == expected_big
    assert codec.serialize(value, endianes=Endianes.LITTLE) == expected_little


@pytest.mark.parametrize(
    "bits_big, bits_little, expected",
    [
        (string_to_bits("01000001"), string_to_bits("01000001"), b"A"),
        (string_to_bits("0110000101100010"), string_to_bits("0110001001100001"), b"ab"),
        (
            string_to_bits("0000000011111111"),
            string_to_bits("1111111100000000"),
            b"\x00\xff",
        ),
    ],
)
def test_data_deserialize(bits_big: Bits, bits_little: Bits, expected: bytes) -> None:
    codec = DataCodec()

    buffer = BitBuffer()
    buffer.write(bits_big)
    result = codec.deserialize(buffer, endianes=Endianes.BIG)
    assert result == expected

    buffer = BitBuffer()
    buffer.write(bits_little)
    result = codec.deserialize(buffer, endianes=Endianes.LITTLE)
    assert result == expected


@pytest.mark.parametrize("value", [b"", b"A", b"abc", bytes([1, 2, 3, 4])])
def test_data_roundtrip(value: bytes) -> None:
    codec = DataCodec()
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        bits: Bits = codec.serialize(value, endianes=endianes)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == value
