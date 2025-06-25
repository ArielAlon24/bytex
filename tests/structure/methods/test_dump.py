import pytest
from utils import _create_codecs, _create_instance, Values, Value

from bytex import Endianes
from bytex.errors import AlignmentError
from bytex.codecs import IntegerCodec
from bytex import Sign
from bytex._structure.methods import _create_dump


@pytest.mark.parametrize(
    ("values", "endianes", "expected_bytes"),
    [
        (
            {
                "a": Value(codec=IntegerCodec(8, Sign.SIGNED), value=20),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=128),
            },
            Endianes.BIG,
            b"\x14\x00\x80",
        ),
        (
            {
                "a": Value(codec=IntegerCodec(8, Sign.UNSIGNED), value=0xAB),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=0x1234),
            },
            Endianes.LITTLE,
            b"\x34\x12\xab",
        ),
        (
            {
                "x": Value(codec=IntegerCodec(8, Sign.SIGNED), value=-1),
                "y": Value(codec=IntegerCodec(8, Sign.SIGNED), value=-128),
            },
            Endianes.BIG,
            b"\xff\x80",
        ),
        (
            {
                "a": Value(codec=IntegerCodec(16, Sign.SIGNED), value=-2),
                "b": Value(codec=IntegerCodec(8, Sign.UNSIGNED), value=255),
            },
            Endianes.LITTLE,
            b"\xff\xfe\xff",
        ),
        (
            {
                "a": Value(codec=IntegerCodec(24, Sign.UNSIGNED), value=0x123456),
            },
            Endianes.BIG,
            b"\x12\x34\x56",
        ),
        (
            {
                "a": Value(codec=IntegerCodec(24, Sign.UNSIGNED), value=0x123456),
            },
            Endianes.LITTLE,
            b"\x56\x34\x12",
        ),
        (
            {
                "a": Value(codec=IntegerCodec(8, Sign.UNSIGNED), value=0x11),
                "b": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=0x2233),
                "c": Value(codec=IntegerCodec(32, Sign.UNSIGNED), value=0x44556677),
            },
            Endianes.LITTLE,
            b"\x77\x66\x55\x44\x33\x22\x11",
        ),
    ],
)
def test_dump_success(values: Values, endianes: Endianes, expected_bytes: bytes):
    fields = _create_codecs(values)
    instance = _create_instance(values)
    dump_method = _create_dump(fields)
    data = dump_method(instance, endianes)
    assert data == expected_bytes, f"{data.hex()} != {expected_bytes.hex()}"


@pytest.mark.parametrize(
    ("values", "endianes", "expected_message"),
    [
        (
            {
                "a": Value(codec=IntegerCodec(8, Sign.SIGNED), value=0),
                "b": Value(codec=IntegerCodec(15, Sign.UNSIGNED), value=0),
            },
            Endianes.BIG,
            "Cannot dump a structure whose bit size is not a multiple of 8",
        ),
        (
            {
                "a": Value(codec=IntegerCodec(4, Sign.UNSIGNED), value=1),
                "b": Value(codec=IntegerCodec(4, Sign.UNSIGNED), value=2),
                "c": Value(codec=IntegerCodec(1, Sign.UNSIGNED), value=0),
            },
            Endianes.LITTLE,
            "Cannot dump a structure whose bit size is not a multiple of 8",
        ),
        (
            {
                "a": Value(codec=IntegerCodec(7, Sign.UNSIGNED), value=0),
            },
            Endianes.BIG,
            "Cannot dump a structure whose bit size is not a multiple of 8",
        ),
        (
            {
                "x": Value(codec=IntegerCodec(16, Sign.SIGNED), value=123),
                "y": Value(codec=IntegerCodec(16, Sign.UNSIGNED), value=456),
                "z": Value(codec=IntegerCodec(4, Sign.UNSIGNED), value=5),
            },
            Endianes.LITTLE,
            "Cannot dump a structure whose bit size is not a multiple of 8",
        ),
    ],
)
def test_dump_failure(values: Values, endianes: Endianes, expected_message: str):
    fields = _create_codecs(values)
    instance = _create_instance(values)
    dump_method = _create_dump(fields)

    with pytest.raises(AlignmentError) as exc_info:
        dump_method(instance, endianes)

    assert expected_message == str(exc_info.value)
