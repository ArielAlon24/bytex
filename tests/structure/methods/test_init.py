import pytest
from utils import _create_empty_instance

from typing import Any, Dict

from structure._structure.types import Codecs
from structure._structure.method_creators import _create_init
from structure.codecs import IntegerCodec
from structure import Sign
from structure.errors import ValidationError


@pytest.mark.parametrize(
    ("name", "codecs", "input_data"),
    [
        (
            "Point",
            {
                "x": IntegerCodec(bit_count=8, sign=Sign.SIGNED),
                "y": IntegerCodec(bit_count=8, sign=Sign.UNSIGNED),
            },
            {"x": -5, "y": 10},
        ),
        (
            "SingleField",
            {
                "id": IntegerCodec(bit_count=16, sign=Sign.UNSIGNED),
            },
            {"id": 42},
        ),
    ],
)
def test_create_init_success(
    name: str,
    codecs: Codecs,
    input_data: Dict[str, Any],
):
    instance = _create_empty_instance(name)
    init_method = _create_init(codecs)
    init_method(instance, **input_data)  # type: ignore

    for key, expected_value in input_data.items():
        assert getattr(instance, key) == expected_value


@pytest.mark.parametrize(
    "codecs, actual, expected_message",
    [
        (
            {"a": IntegerCodec(8, Sign.UNSIGNED), "b": IntegerCodec(8, Sign.UNSIGNED)},
            {"a": 1},
            "Invalid constructor arguments - Missing field: 'b'",
        ),
        (
            {
                "a": IntegerCodec(8, Sign.UNSIGNED),
                "b": IntegerCodec(8, Sign.UNSIGNED),
            },
            {"a": 1, "c": 3},
            "Invalid constructor arguments - Missing field: 'b'; Unexpected field: 'c'",
        ),
        (
            {
                "x": IntegerCodec(8, Sign.UNSIGNED),
                "y": IntegerCodec(8, Sign.UNSIGNED),
                "z": IntegerCodec(8, Sign.UNSIGNED),
            },
            {"a": 1, "b": 2},
            "Invalid constructor arguments - Missing fields: 'x', 'y', 'z'; Unexpected fields: 'a', 'b'",
        ),
        (
            {"a": IntegerCodec(8, Sign.UNSIGNED), "b": IntegerCodec(8, Sign.UNSIGNED)},
            {"a": 1, "b": 2, "c": 3},
            "Invalid constructor arguments - Unexpected field: 'c'",
        ),
    ],
)
def test_init_failure(codecs: Codecs, actual: Dict[str, Any], expected_message: str):
    instance = _create_empty_instance()
    init_method = _create_init(codecs)

    with pytest.raises(ValidationError) as exc_info:
        init_method(instance, **actual)  # type: ignore

    assert expected_message == str(exc_info.value)
