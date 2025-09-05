from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.codecs.prefix.prefix_string_codec import PrefixStringCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError
from bytex.sign import Sign


@pytest.mark.parametrize("value", ["", "A", "ab", "xyz"])
def test_prefix_string_validate_success(value: str) -> None:
    codec = PrefixStringCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)
    )
    codec.validate(value)


@pytest.mark.parametrize("value", [None, 123, True, b"A"])
def test_prefix_string_validate_failure(value: Any) -> None:
    codec = PrefixStringCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)
    )
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("A", string_to_bits("0000000101000001")),
        ("ab", string_to_bits("000000100110000101100010")),
        ("01", string_to_bits("000000100011000000110001")),
    ],
)
def test_prefix_string_serialize(value: str, expected: Bits) -> None:
    codec = PrefixStringCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        assert codec.serialize(value, endianness=endianness) == expected


@pytest.mark.parametrize(
    "bits, expected",
    [
        (string_to_bits("0000000101000001"), "A"),
        (string_to_bits("000000100110000101100010"), "ab"),
        (string_to_bits("000000100011000000110001"), "01"),
    ],
)
def test_prefix_string_deserialize(bits: Bits, expected: str) -> None:
    codec = PrefixStringCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == expected


@pytest.mark.parametrize("value", ["", "A", "ab", "01", "xyz"])
def test_prefix_string_roundtrip(value: str) -> None:
    codec = PrefixStringCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED)
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        bits: Bits = codec.serialize(value, endianness=endianness)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == value
