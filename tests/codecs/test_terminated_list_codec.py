from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.basic.char_codec import CharCodec
from bytex.codecs.terminated.terminated_list_codec import TerminatedListCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError

TERMINATOR: Bits = string_to_bits("00000000")


@pytest.mark.parametrize("value", [[], ["A"], ["a", "b"], ["x", "y", "z"]])
def test_terminated_list_validate_success(value: list[str]) -> None:
    codec = TerminatedListCodec(item_codec=CharCodec(), terminator=TERMINATOR)
    codec.validate(value)


@pytest.mark.parametrize("value", [None, 123, True, object()])
def test_terminated_list_validate_failure(value: Any) -> None:
    codec = TerminatedListCodec(item_codec=CharCodec(), terminator=TERMINATOR)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (["A"], string_to_bits("0100000100000000")),
        (["a", "b"], string_to_bits("011000010110001000000000")),
        (["x", "y", "z"], string_to_bits("01111000011110010111101000000000")),
    ],
)
def test_terminated_list_serialize(value: list[str], expected: Bits) -> None:
    codec = TerminatedListCodec(item_codec=CharCodec(), terminator=TERMINATOR)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        assert codec.serialize(value, endianes=endianes) == expected


@pytest.mark.parametrize(
    "bits, expected",
    [
        (string_to_bits("0100000100000000"), ["A"]),
        (string_to_bits("011000010110001000000000"), ["a", "b"]),
        (string_to_bits("01111000011110010111101000000000"), ["x", "y", "z"]),
    ],
)
def test_terminated_list_deserialize(bits: Bits, expected: list[str]) -> None:
    codec = TerminatedListCodec(item_codec=CharCodec(), terminator=TERMINATOR)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == expected


@pytest.mark.parametrize("value", [[], ["A"], ["a", "b"], ["x", "y", "z"]])
def test_terminated_list_roundtrip(value: list[str]) -> None:
    codec = TerminatedListCodec(item_codec=CharCodec(), terminator=TERMINATOR)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        bits: Bits = codec.serialize(value, endianes=endianes)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == value
