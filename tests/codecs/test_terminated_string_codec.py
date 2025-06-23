import pytest
from structure.bit_buffer import BitBuffer, Bits
from structure.codecs.terminated_string_codec import TerminatedStringCodec
from structure.errors import ValidationError
from utils import bits_to_string, string_to_bits


@pytest.mark.parametrize("terminator", ["\0", "!!", "END"])
@pytest.mark.parametrize("value", ["", "abc", "hello world", "1234567890"])
def test_validate_success(value, terminator):
    codec = TerminatedStringCodec(terminator)
    assert terminator not in value
    codec.validate(value)


@pytest.mark.parametrize("value", [123, None, b"bytes"])
def test_validate_wrong_type(value):
    codec = TerminatedStringCodec("\0")
    with pytest.raises(ValidationError, match="value must be of type"):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, terminator",
    [
        ("hello\0world", "\0"),
        ("abc!!def", "!!"),
        ("thisENDthat", "END"),
    ],
)
def test_validate_contains_terminator(value, terminator):
    codec = TerminatedStringCodec(terminator)
    with pytest.raises(ValidationError, match="must not contain the terminator"):
        codec.validate(value)


@pytest.mark.parametrize(
    "value, terminator",
    [
        ("hello", "\0"),
        ("abc", "!"),
        ("data123", "END"),
        ("", "X"),
    ],
)
def test_serialize_deserialize_roundtrip(value, terminator):
    codec = TerminatedStringCodec(terminator)
    bits = codec.serialize(value)
    buffer = BitBuffer()
    buffer.write(bits)
    result = codec.deserialize(buffer)
    assert result == value


@pytest.mark.parametrize(
    "value, terminator, expected_bits",
    [
        (
            "A",
            "\0",
            string_to_bits("0100000100000000"),
        ),
        (
            "Hi",
            "!",
            string_to_bits("010010000110100100100001"),
        ),
    ],
)
def test_serialize_output(value, terminator, expected_bits):
    codec = TerminatedStringCodec(terminator)
    bits = codec.serialize(value)
    assert (
        bits == expected_bits
    ), f"{bits_to_string(bits)} != {bits_to_string(expected_bits)}"


def test_deserialize_with_terminator_only():
    codec = TerminatedStringCodec("\0")
    buffer = BitBuffer()
    buffer.write([False] * 8)
    result = codec.deserialize(buffer)
    assert result == ""


def test_bit_remainder():
    codec = TerminatedStringCodec("\0")
    assert codec.bit_remainder() == 0


def test_repr():
    codec = TerminatedStringCodec("XYZ")
    assert repr(codec) == "TerminatedString('XYZ')"
