from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.basic.char_codec import CharCodec
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.codecs.prefix.prefix_list_codec import PrefixListCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError
from bytex.sign import Sign


@pytest.mark.parametrize("value", [[], ["A"], ["a", "b"], ["x", "y", "z"]])
def test_prefix_list_validate_success(value: list[str]) -> None:
    codec = PrefixListCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED),
        item_codec=CharCodec(),
    )
    codec.validate(value)


@pytest.mark.parametrize("value", [None, object(), 123, True])
def test_prefix_list_validate_failure(value: Any) -> None:
    codec = PrefixListCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED),
        item_codec=CharCodec(),
    )
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (["A"], string_to_bits("0000000101000001")),
        (["a", "b"], string_to_bits("000000100110000101100010")),
        (["x", "y", "z"], string_to_bits("00000011011110000111100101111010")),
    ],
)
def test_prefix_list_serialize(value: list[str], expected: Bits) -> None:
    codec = PrefixListCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED),
        item_codec=CharCodec(),
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        assert codec.serialize(value, endianness=endianness) == expected


@pytest.mark.parametrize(
    "bits, expected",
    [
        (string_to_bits("0000000101000001"), ["A"]),
        (string_to_bits("000000100110000101100010"), ["a", "b"]),
        (string_to_bits("00000011011110000111100101111010"), ["x", "y", "z"]),
    ],
)
def test_prefix_list_deserialize(bits: Bits, expected: list[str]) -> None:
    codec = PrefixListCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED),
        item_codec=CharCodec(),
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == expected


@pytest.mark.parametrize("value", [[], ["A"], ["a", "b"], ["x", "y", "z"]])
def test_prefix_list_roundtrip(value: list[str]) -> None:
    codec = PrefixListCodec(
        prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED),
        item_codec=CharCodec(),
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        bits = codec.serialize(value, endianness=endianness)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == value
