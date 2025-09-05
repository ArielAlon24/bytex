from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.terminated.terminated_string_codec import TerminatedStringCodec
from bytex.endianness import Endianness
from bytex.errors import ValidationError

TERMINATOR: Bits = string_to_bits("00000000")


@pytest.mark.parametrize("value", ["", "A", "abc", "xyz"])
def test_terminated_string_validate_success(value: str) -> None:
    codec = TerminatedStringCodec(terminator=TERMINATOR)
    codec.validate(value)


@pytest.mark.parametrize("value", [None, 123, True, b"A"])
def test_terminated_string_validate_failure_type(value: Any) -> None:
    codec = TerminatedStringCodec(terminator=TERMINATOR)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize("value", ["\x00", "A\x00", "abc\x00"])
def test_terminated_string_validate_failure_contains_terminator(value: str) -> None:
    codec = TerminatedStringCodec(terminator=TERMINATOR)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("A", string_to_bits("0100000100000000")),
        ("ab", string_to_bits("011000010110001000000000")),
        ("01", string_to_bits("001100000011000100000000")),
    ],
)
def test_terminated_string_serialize(value: str, expected: Bits) -> None:
    codec = TerminatedStringCodec(terminator=TERMINATOR)
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        assert codec.serialize(value, endianness=endianness) == expected


@pytest.mark.parametrize(
    "bits, expected",
    [
        (string_to_bits("0100000100000000"), "A"),
        (string_to_bits("011000010110001000000000"), "ab"),
        (string_to_bits("001100000011000100000000"), "01"),
    ],
)
def test_terminated_string_deserialize(bits: Bits, expected: str) -> None:
    codec = TerminatedStringCodec(terminator=TERMINATOR)
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == expected


@pytest.mark.parametrize("value", ["", "A", "ab", "01", "xyz"])
def test_terminated_string_roundtrip(value: str) -> None:
    codec = TerminatedStringCodec(terminator=TERMINATOR)
    for endianness in (Endianness.BIG, Endianness.LITTLE):
        bits: Bits = codec.serialize(value, endianness=endianness)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianness=endianness)
        assert result == value
