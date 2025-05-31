import pytest
from unittest.mock import MagicMock
from structure.errors import ParsingError
from utils import _create_codecs, Values, Value

from structure import Endianes
from structure.codecs import IntegerCodec
from structure import Sign
from structure._structure.method_creators import _create_parse


@pytest.mark.parametrize(
    ("bytes_data", "values", "endianes"),
    [
        (
            b"\x14\x00\x80",
            {
                "a": Value(codec=IntegerCodec(8, Sign.SIGNED), value=20),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=128),
            },
            Endianes.BIG,
        ),
        (
            b"\x34\x12\xab",
            {
                "a": Value(codec=IntegerCodec(8, Sign.UNSIGNED), value=0xAB),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=0x1234),
            },
            Endianes.LITTLE,
        ),
        (
            b"\xff\x80",
            {
                "x": Value(codec=IntegerCodec(8, Sign.SIGNED), value=-1),
                "y": Value(codec=IntegerCodec(8, Sign.SIGNED), value=-128),
            },
            Endianes.BIG,
        ),
        (
            b"\xff\xfe\xff",
            {
                "a": Value(codec=IntegerCodec(16, Sign.SIGNED), value=-2),
                "b": Value(codec=IntegerCodec(8, Sign.UNSIGNED), value=255),
            },
            Endianes.LITTLE,
        ),
        (
            b"\x12\x34\x56",
            {
                "a": Value(codec=IntegerCodec(24, Sign.UNSIGNED), value=0x123456),
            },
            Endianes.BIG,
        ),
        (
            b"\x56\x34\x12",
            {
                "a": Value(codec=IntegerCodec(24, Sign.UNSIGNED), value=0x123456),
            },
            Endianes.LITTLE,
        ),
        (
            b"\x77\x66\x55\x44\x33\x22\x11",
            {
                "a": Value(codec=IntegerCodec(8, Sign.UNSIGNED), value=0x11),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=0x2233),
                "c": Value(codec=IntegerCodec(32, Sign.UNSIGNED), value=0x44556677),
            },
            Endianes.LITTLE,
        ),
    ],
)
def test_parse_success(bytes_data: bytes, values: Values, endianes: Endianes):
    fields = _create_codecs(values)
    _type = MagicMock()

    _type.parse = _create_parse(fields)

    _type.parse.__get__(None, _type)(bytes_data, endianes)  # type: ignore

    _type.assert_called_once_with(
        **{name: value.value for name, value in values.items()}
    )


@pytest.mark.parametrize(
    ("data", "values", "endianes", "expected_message"),
    [
        (
            b"\x14\x00\x80\x00",
            {
                "a": Value(codec=IntegerCodec(8, Sign.SIGNED), value=20),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=128),
            },
            Endianes.BIG,
            "Unexpected trailing data: 8 bits left",
        ),
        (
            b"\x14\x00\x80\xf0",
            {
                "a": Value(codec=IntegerCodec(8, Sign.SIGNED), value=20),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=128),
            },
            Endianes.LITTLE,
            "Unexpected trailing data: 8 bits left",
        ),
        (
            b"\x14\x00",
            {
                "a": Value(codec=IntegerCodec(8, Sign.SIGNED), value=20),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=128),
            },
            Endianes.BIG,
            "Insufficient data while parsing field 'b'",
        ),
        (
            b"\x01\x02\x03\x04",
            {
                "a": Value(codec=IntegerCodec(8, Sign.UNSIGNED), value=1),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=0x0203),
            },
            Endianes.BIG,
            "Unexpected trailing data: 8 bits left",
        ),
    ],
)
def test_parse_failure(
    data: bytes, values: Values, endianes: Endianes, expected_message: str
):
    fields = _create_codecs(values)
    _type = MagicMock()

    _type.parse = _create_parse(fields)

    with pytest.raises(ParsingError) as exc_info:
        _type.parse.__get__(None, _type)(data, endianes=endianes, strict=True)  # type: ignore

    assert expected_message == str(exc_info.value)
