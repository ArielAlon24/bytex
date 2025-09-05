from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.basic.char_codec import CharCodec
from bytex.codecs.exact.exact_list_codec import ExactListCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError


@pytest.mark.parametrize("value, length", [(["A"], 1), (["a", "b"], 2)])
def test_exact_list_validate_success(value: list[str], length: int) -> None:
    codec = ExactListCodec(item_codec=CharCodec(), length=length)
    codec.validate(value)


@pytest.mark.parametrize("value, length", [(["A"], 2), ("AB", 1), (123, 1)])
def test_exact_list_validate_failure(value: Any, length: int) -> None:
    codec = ExactListCodec(item_codec=CharCodec(), length=length)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, length, expected",
    [
        (["A"], 1, string_to_bits("01000001")),
        (["a", "b"], 2, string_to_bits("0110000101100010")),
        (["A", "a"], 2, string_to_bits("0100000101100001")),
    ],
)
def test_exact_list_serialize(value: list[str], length: int, expected: Bits) -> None:
    codec = ExactListCodec(item_codec=CharCodec(), length=length)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        assert codec.serialize(value, endianes=endianes) == expected


@pytest.mark.parametrize(
    "length, bits, expected",
    [
        (1, string_to_bits("01000001"), ["A"]),
        (2, string_to_bits("0110000101100010"), ["a", "b"]),
        (2, string_to_bits("0100000101100001"), ["A", "a"]),
    ],
)
def test_exact_list_deserialize(length: int, bits: Bits, expected: list[str]) -> None:
    codec = ExactListCodec(item_codec=CharCodec(), length=length)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == expected


@pytest.mark.parametrize(
    "value, length", [(["A"], 1), (["a", "b"], 2), (["A", "a"], 2)]
)
def test_exact_list_roundtrip(value: list[str], length: int) -> None:
    codec = ExactListCodec(item_codec=CharCodec(), length=length)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        bits = codec.serialize(value, endianes=endianes)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == value
