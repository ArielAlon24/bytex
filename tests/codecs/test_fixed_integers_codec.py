from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.codecs.fixed.fixed_integers_codec import FixedIntegersCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError
from bytex.sign import Sign


@pytest.mark.parametrize("value, length", [([1], 1), ([1, 2], 2), ([0x7F, -1], 2)])
def test_fixed_integers_validate_success(value: list[int], length: int) -> None:
    codec = FixedIntegersCodec(
        integer_codec=IntegerCodec(8, Sign.SIGNED), length=length
    )
    codec.validate(value)


@pytest.mark.parametrize("value, length", [([1, 2, 3], 2), ("1,2", 2), (123, 1)])
def test_fixed_integers_validate_failure(value: Any, length: int) -> None:
    codec = FixedIntegersCodec(
        integer_codec=IntegerCodec(8, Sign.UNSIGNED), length=length
    )
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, length, expected",
    [
        ([65], 2, string_to_bits("0100000100000000")),
        ([97, 98], 2, string_to_bits("0110000101100010")),
        ([0, 255], 2, string_to_bits("0000000011111111")),
    ],
)
def test_fixed_integers_serialize(
    value: list[int], length: int, expected: Bits
) -> None:
    codec = FixedIntegersCodec(
        integer_codec=IntegerCodec(8, Sign.UNSIGNED), length=length
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        assert codec.serialize(value, endianness=endianness) == expected


@pytest.mark.parametrize(
    "length, bits, expected",
    [
        (2, string_to_bits("0100000100000000"), [65, 0]),
        (2, string_to_bits("0110000101100010"), [97, 98]),
        (2, string_to_bits("0000000011111111"), [0, 255]),
    ],
)
def test_fixed_integers_deserialize(
    length: int, bits: Bits, expected: list[int]
) -> None:
    codec = FixedIntegersCodec(
        integer_codec=IntegerCodec(8, Sign.UNSIGNED), length=length
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == expected


@pytest.mark.parametrize(
    "value, length", [([65], 2), ([97, 98], 2), ([0, 255], 2), ([1, 2, 3], 4)]
)
def test_fixed_integers_roundtrip(value: list[int], length: int) -> None:
    codec = FixedIntegersCodec(
        integer_codec=IntegerCodec(8, Sign.UNSIGNED), length=length
    )
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        bits: Bits = codec.serialize(value, endianness=endianness)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        padded = value + [0] * (length - len(value))
        assert result == padded


@pytest.mark.parametrize(
    "integer_bits, value, expected_big, expected_little",
    [
        (
            16,
            [0x1234],
            string_to_bits("0001001000110100"),
            string_to_bits("0011010000010010"),
        ),
        (
            32,
            [0x12345678],
            string_to_bits("00010010001101000101011001111000"),
            string_to_bits("01111000010101100011010000010010"),
        ),
    ],
)
def test_fixed_integers_endian_item_order(
    integer_bits: int, value: list[int], expected_big: Bits, expected_little: Bits
) -> None:
    codec = FixedIntegersCodec(
        integer_codec=IntegerCodec(integer_bits, Sign.UNSIGNED), length=1
    )

    assert codec.serialize(value, endianness=Endianness.BIG) == expected_big
    assert codec.serialize(value, endianness=Endianness.LITTLE) == expected_little

    buffer = BitBuffer()
    buffer.write(expected_big)
    result_big = codec.deserialize(buffer, endianness=Endianness.BIG)
    assert result_big == value

    buffer = BitBuffer()
    buffer.write(expected_little)
    result_little = codec.deserialize(buffer, endianness=Endianness.LITTLE)
    assert result_little == value


def test_fixed_integers_list_order_preserved() -> None:
    codec = FixedIntegersCodec(integer_codec=IntegerCodec(16, Sign.UNSIGNED), length=2)
    values = [0x1234, 0xABCD]

    bits_big = codec.serialize(values, endianness=Endianness.BIG)
    bits_little = codec.serialize(values, endianness=Endianness.LITTLE)

    buffer = BitBuffer()
    buffer.write(bits_big)
    assert codec.deserialize(buffer, endianness=Endianness.BIG) == values

    buffer = BitBuffer()
    buffer.write(bits_little)
    assert codec.deserialize(buffer, endianness=Endianness.LITTLE) == values
