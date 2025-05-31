import pytest
from utils import Value, _create_codecs, _create_instance, Values

from structure._structure.method_creators import _create_repr
from structure.codecs import IntegerCodec
from structure import Sign


@pytest.mark.parametrize(
    ("name", "values", "expected_repr"),
    [
        (
            "Mixed",
            {
                "a": Value(codec=IntegerCodec(bit_count=8, sign=Sign.SIGNED), value=20),
                "b": Value(
                    codec=IntegerCodec(bit_count=16, sign=Sign.UNSIGNED), value=128
                ),
            },
            "Mixed(a: I8 = 20, b: U16 = 128)",
        ),
        (
            "SignedNegative",
            {
                "x": Value(codec=IntegerCodec(bit_count=8, sign=Sign.SIGNED), value=-5),
                "y": Value(codec=IntegerCodec(bit_count=4, sign=Sign.SIGNED), value=-1),
            },
            "SignedNegative(x: I8 = -5, y: I4 = -1)",
        ),
        (
            "UnsignedOnly",
            {
                "val": Value(
                    codec=IntegerCodec(bit_count=12, sign=Sign.UNSIGNED), value=4095
                ),
            },
            "UnsignedOnly(val: U12 = 4095)",
        ),
        (
            "MaxBitWidth",
            {
                "m": Value(
                    codec=IntegerCodec(bit_count=24, sign=Sign.UNSIGNED),
                    value=(1 << 24) - 1,
                ),
                "n": Value(
                    codec=IntegerCodec(bit_count=32, sign=Sign.SIGNED), value=-(1 << 31)
                ),
            },
            "MaxBitWidth(m: U24 = 16777215, n: I32 = -2147483648)",
        ),
        (
            "ZeroValues",
            {
                "z1": Value(codec=IntegerCodec(bit_count=8, sign=Sign.SIGNED), value=0),
                "z2": Value(
                    codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED), value=0
                ),
            },
            "ZeroValues(z1: I8 = 0, z2: U8 = 0)",
        ),
    ],
)
def test_repr(name: str, values: Values, expected_repr: str):
    codecs = _create_codecs(values)
    instance = _create_instance(name=name, values=values)
    repr_method = _create_repr(codecs)

    assert repr_method(instance) == expected_repr
