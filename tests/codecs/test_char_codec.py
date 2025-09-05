from typing import Any

import pytest

from bytex import BitBuffer
from bytex.bits import Bits, string_to_bits
from bytex.codecs.basic.char_codec import CharCodec
from bytex.endianes import Endianes
from bytex.errors import ValidationError


@pytest.mark.parametrize("value", ["A", "z", "0", " ", "\n"])
def test_char_validate_success(value: str) -> None:
    codec = CharCodec()
    codec.validate(value)


@pytest.mark.parametrize("value", [None, "", "AB", 5, True, [], {}])
def test_char_validate_failure(value: Any) -> None:
    codec = CharCodec()
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize(
    "char, expected_bits",
    [
        ("A", string_to_bits("01000001")),
        ("a", string_to_bits("01100001")),
        ("0", string_to_bits("00110000")),
        (" ", string_to_bits("00100000")),
    ],
)
def test_char_serialize(char: str, expected_bits: Bits) -> None:
    codec = CharCodec()

    assert codec.serialize(char, endianes=Endianes.BIG) == expected_bits


@pytest.mark.parametrize(
    "bits, char",
    [
        (string_to_bits("01000001"), "A"),
        (string_to_bits("01100001"), "a"),
        (string_to_bits("00110000"), "0"),
        (string_to_bits("00100000"), " "),
    ],
)
def test_char_deserialize(bits: Bits, char: str) -> None:
    codec = CharCodec()
    buffer = BitBuffer()
    buffer.write(bits)
    result = codec.deserialize(buffer, endianes=Endianes.LITTLE)
    assert result == char


@pytest.mark.parametrize("char", ["A", "a", "0", " ", "\n"])
def test_char_roundtrip(char: str) -> None:
    codec = CharCodec()
    bits = codec.serialize(char, endianes=Endianes.BIG)

    buffer = BitBuffer()
    buffer.write(bits)
    result = codec.deserialize(buffer, endianes=Endianes.LITTLE)

    assert result == char
