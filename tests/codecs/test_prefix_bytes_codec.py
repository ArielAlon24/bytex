from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.basic.integer_codec import IntegerCodec
from bytex.codecs.prefix.prefix_bytes_codec import PrefixBytesCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError
from bytex.sign import Sign


@pytest.mark.parametrize("value", [b"", b"A", b"abc", bytes([1, 2, 3])])
def test_prefix_bytes_validate_success(value: bytes) -> None:
    codec = PrefixBytesCodec(prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED))
    codec.validate(value)


@pytest.mark.parametrize("value", [None, "A", 123, True, ["a"], {"k": b"v"}])
def test_prefix_bytes_validate_failure(value: Any) -> None:
    codec = PrefixBytesCodec(prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED))
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (b"A", string_to_bits("0000000101000001")),
        (b"ab", string_to_bits("000000100110000101100010")),
        (b"\x00\xff", string_to_bits("000000100000000011111111")),
    ],
)
def test_prefix_bytes_serialize(value: bytes, expected: Bits) -> None:
    codec = PrefixBytesCodec(prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED))
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        assert codec.serialize(value, endianness=endianness) == expected


@pytest.mark.parametrize(
    "bits, expected",
    [
        (string_to_bits("0000000101000001"), b"A"),
        (string_to_bits("000000100110000101100010"), b"ab"),
        (string_to_bits("000000100000000011111111"), b"\x00\xff"),
    ],
)
def test_prefix_bytes_deserialize(bits: Bits, expected: bytes) -> None:
    codec = PrefixBytesCodec(prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED))
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == expected


@pytest.mark.parametrize("value", [b"", b"A", b"ab", b"\x00\xff", bytes([1, 2, 3])])
def test_prefix_bytes_roundtrip(value: bytes) -> None:
    codec = PrefixBytesCodec(prefix_codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED))
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        bits: Bits = codec.serialize(value, endianness=endianness)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == value
