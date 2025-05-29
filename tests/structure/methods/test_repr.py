import pytest
from utils import _create_fields, _create_instance, Values

from structure._structure.method_creators import _create_repr
from structure.codecs import IntegerCodec
from structure import Sign
from structure.data_types.base_data_type import BaseDataType
from structure.data_types import Integer


@pytest.mark.parametrize(
    ("name", "values", "expected_repr"),
    [
        (
            "Mixed",
            {
                "a": Integer(
                    codec=IntegerCodec(bit_count=8, sign=Sign.SIGNED), value=20
                ),
                "b": Integer(
                    codec=IntegerCodec(bit_count=16, sign=Sign.UNSIGNED), value=128
                ),
            },
            "Mixed(a: I8 = 20, b: U16 = 128)",
        ),
        (
            "SignedNegative",
            {
                "x": Integer(
                    codec=IntegerCodec(bit_count=8, sign=Sign.SIGNED), value=-5
                ),
                "y": Integer(
                    codec=IntegerCodec(bit_count=4, sign=Sign.SIGNED), value=-1
                ),
            },
            "SignedNegative(x: I8 = -5, y: I4 = -1)",
        ),
        (
            "UnsignedOnly",
            {
                "val": Integer(
                    codec=IntegerCodec(bit_count=12, sign=Sign.UNSIGNED), value=4095
                ),
            },
            "UnsignedOnly(val: U12 = 4095)",
        ),
        (
            "MaxBitWidth",
            {
                "m": Integer(
                    codec=IntegerCodec(bit_count=24, sign=Sign.UNSIGNED),
                    value=(1 << 24) - 1,
                ),
                "n": Integer(
                    codec=IntegerCodec(bit_count=32, sign=Sign.SIGNED), value=-(1 << 31)
                ),
            },
            "MaxBitWidth(m: U24 = 16777215, n: I32 = -2147483648)",
        ),
        (
            "ZeroValues",
            {
                "z1": Integer(
                    codec=IntegerCodec(bit_count=8, sign=Sign.SIGNED), value=0
                ),
                "z2": Integer(
                    codec=IntegerCodec(bit_count=8, sign=Sign.UNSIGNED), value=0
                ),
            },
            "ZeroValues(z1: I8 = 0, z2: U8 = 0)",
        ),
    ],
)
def test_repr(name: str, values: Values, expected_repr: str):
    fields = _create_fields(values)
    instance = _create_instance(name=name, values=values)
    repr_method = _create_repr(fields)

    assert repr_method(instance) == expected_repr
