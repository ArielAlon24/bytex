from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.terminated.terminated_bytes_codec import TerminatedBytesCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError

TERMINATOR: Bits = string_to_bits("00000000")


@pytest.mark.parametrize("value", [b"", b"A", b"abc", bytes([1, 2, 3])])
def test_terminated_bytes_validate_success(value: bytes) -> None:
    codec = TerminatedBytesCodec(terminator=TERMINATOR)
    codec.validate(value)


@pytest.mark.parametrize("value", [None, "A", 123, True])
def test_terminated_bytes_validate_failure_type(value: Any) -> None:
    codec = TerminatedBytesCodec(terminator=TERMINATOR)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize("value", [b"\x00", b"A\x00", b"abc\x00"])
def test_terminated_bytes_validate_failure_contains_terminator(value: bytes) -> None:
    codec = TerminatedBytesCodec(terminator=TERMINATOR)
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (b"A", string_to_bits("0100000100000000")),
        (b"ab", string_to_bits("011000010110001000000000")),
        (b"\x01\x02", string_to_bits("000000010000001000000000")),
    ],
)
def test_terminated_bytes_serialize(value: bytes, expected: Bits) -> None:
    codec = TerminatedBytesCodec(terminator=TERMINATOR)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        assert codec.serialize(value, endianes=endianes) == expected


@pytest.mark.parametrize(
    "bits, expected",
    [
        (string_to_bits("0100000100000000"), b"A"),
        (string_to_bits("011000010110001000000000"), b"ab"),
        (string_to_bits("000000010000001000000000"), b"\x01\x02"),
    ],
)
def test_terminated_bytes_deserialize(bits: Bits, expected: bytes) -> None:
    codec = TerminatedBytesCodec(terminator=TERMINATOR)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == expected


@pytest.mark.parametrize("value", [b"", b"A", b"ab", bytes([1, 2, 3])])
def test_terminated_bytes_roundtrip(value: bytes) -> None:
    codec = TerminatedBytesCodec(terminator=TERMINATOR)
    for endianes in (Endianes.BIG, Endianes.LITTLE):
        bits: Bits = codec.serialize(value, endianes=endianes)
        buffer = BitBuffer()
        buffer.write(bits)
        result = codec.deserialize(buffer, endianes=endianes)
        assert result == value
