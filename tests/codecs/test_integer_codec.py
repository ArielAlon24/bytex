import pytest
from bytex import Sign, BitBuffer
from bytex.codecs import IntegerCodec
from bytex.errors import ValidationError


@pytest.mark.parametrize(
    "number, value",
    [
        (IntegerCodec(bit_count=4, sign=Sign.UNSIGNED), 0),
        (IntegerCodec(bit_count=4, sign=Sign.UNSIGNED), (1 << 4) - 1),
        (IntegerCodec(bit_count=4, sign=Sign.SIGNED), -(1 << 3)),
        (IntegerCodec(bit_count=4, sign=Sign.SIGNED), (1 << 3) - 1),
        (IntegerCodec(bit_count=12, sign=Sign.UNSIGNED), (1 << 12) - 1),
        (IntegerCodec(bit_count=12, sign=Sign.SIGNED), -(1 << 11)),
        (IntegerCodec(bit_count=12, sign=Sign.SIGNED), (1 << 11) - 1),
        (IntegerCodec(bit_count=24, sign=Sign.UNSIGNED), 0),
        (IntegerCodec(bit_count=24, sign=Sign.UNSIGNED), (1 << 24) - 1),
        (IntegerCodec(bit_count=24, sign=Sign.SIGNED), -(1 << 23)),
        (IntegerCodec(bit_count=24, sign=Sign.SIGNED), (1 << 23) - 1),
        (IntegerCodec(bit_count=32, sign=Sign.UNSIGNED), 0),
        (IntegerCodec(bit_count=32, sign=Sign.UNSIGNED), (1 << 32) - 1),
        (IntegerCodec(bit_count=32, sign=Sign.SIGNED), -(1 << 31)),
        (IntegerCodec(bit_count=32, sign=Sign.SIGNED), (1 << 31) - 1),
    ],
)
def test_validate_success(number: IntegerCodec, value: int):
    number.validate(value)


@pytest.mark.parametrize(
    "number, value",
    [
        (IntegerCodec(bit_count=4, sign=Sign.UNSIGNED), -1),
        (IntegerCodec(bit_count=4, sign=Sign.UNSIGNED), 1 << 4),
        (IntegerCodec(bit_count=4, sign=Sign.SIGNED), -(1 << 3) - 1),
        (IntegerCodec(bit_count=4, sign=Sign.SIGNED), 1 << 3),
        (IntegerCodec(bit_count=12, sign=Sign.UNSIGNED), 1 << 12),
        (IntegerCodec(bit_count=12, sign=Sign.SIGNED), -(1 << 11) - 1),
        (IntegerCodec(bit_count=12, sign=Sign.SIGNED), 1 << 11),
        (IntegerCodec(bit_count=24, sign=Sign.UNSIGNED), 1 << 24),
        (IntegerCodec(bit_count=24, sign=Sign.SIGNED), -(1 << 23) - 1),
        (IntegerCodec(bit_count=24, sign=Sign.SIGNED), 1 << 23),
        (IntegerCodec(bit_count=32, sign=Sign.UNSIGNED), -1),
        (IntegerCodec(bit_count=32, sign=Sign.UNSIGNED), 1 << 32),
        (IntegerCodec(bit_count=32, sign=Sign.SIGNED), -(1 << 31) - 1),
        (IntegerCodec(bit_count=32, sign=Sign.SIGNED), 1 << 31),
    ],
)
def test_validate_failure(number: IntegerCodec, value: int):
    with pytest.raises(ValidationError):
        number.validate(value)


@pytest.mark.parametrize(
    "bit_count, sign, value, expected_bits",
    [
        (4, Sign.UNSIGNED, 0, [False, False, False, False]),
        (4, Sign.UNSIGNED, 5, [False, True, False, True]),
        (4, Sign.UNSIGNED, 15, [True, True, True, True]),
        (4, Sign.SIGNED, 0, [False, False, False, False]),
        (4, Sign.SIGNED, 7, [False, True, True, True]),
        (4, Sign.SIGNED, -1, [True, True, True, True]),
        (4, Sign.SIGNED, -8, [True, False, False, False]),
        (8, Sign.UNSIGNED, 255, [True] * 8),
        (8, Sign.UNSIGNED, 1, [False] * 7 + [True]),
        (8, Sign.SIGNED, -128, [True] + [False] * 7),
        (8, Sign.SIGNED, 127, [False] + [True] * 7),
    ],
)
def test_serialize(bit_count, sign, value, expected_bits):
    codec = IntegerCodec(bit_count=bit_count, sign=sign)
    bits = codec.serialize(value)
    assert bits == expected_bits


@pytest.mark.parametrize(
    "bit_count, sign, bits, expected_value",
    [
        (4, Sign.UNSIGNED, [False, False, False, False], 0),
        (4, Sign.UNSIGNED, [True, False, True, True], 11),
        (4, Sign.UNSIGNED, [True, True, True, True], 15),
        (4, Sign.SIGNED, [True, False, False, False], -8),
        (4, Sign.SIGNED, [True, True, True, True], -1),
        (4, Sign.SIGNED, [False, True, True, True], 7),
        (8, Sign.UNSIGNED, [False] * 7 + [True], 1),
        (8, Sign.UNSIGNED, [True] * 8, 255),
        (8, Sign.SIGNED, [True] + [False] * 7, -128),
        (8, Sign.SIGNED, [False] + [True] * 7, 127),
    ],
)
def test_deserialize(bit_count, sign, bits, expected_value):
    codec = IntegerCodec(bit_count=bit_count, sign=sign)
    buffer = BitBuffer()
    buffer.write(bits)
    result = codec.deserialize(buffer)
    assert result == expected_value


@pytest.mark.parametrize(
    "bit_count, sign, value",
    [
        (4, Sign.UNSIGNED, 16),
        (4, Sign.UNSIGNED, -1),
        (4, Sign.SIGNED, -9),
        (4, Sign.SIGNED, 8),
        (8, Sign.UNSIGNED, 256),
        (8, Sign.SIGNED, 128),
        (8, Sign.SIGNED, -129),
    ],
)
def test_serialize_validation_error(bit_count, sign, value):
    codec = IntegerCodec(bit_count=bit_count, sign=sign)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "bit_count, sign, value",
    [
        (1, Sign.UNSIGNED, 1),
        (1, Sign.SIGNED, -1),
        (3, Sign.UNSIGNED, 7),
        (3, Sign.SIGNED, -4),
    ],
)
def test_serialize_deserialize_roundtrip(bit_count, sign, value):
    codec = IntegerCodec(bit_count=bit_count, sign=sign)
    bits = codec.serialize(value)
    buffer = BitBuffer()
    buffer.write(bits)
    result = codec.deserialize(buffer)
    assert result == value
