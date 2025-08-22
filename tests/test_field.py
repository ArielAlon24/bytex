from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.base_list_codec import BaseListCodec
from bytex.errors import UninitializedAccessError
from bytex.field import Field


@dataclass
class Context:
    class_type: type
    codec: MagicMock
    list_codec: MagicMock
    list_inner_codec: MagicMock


@pytest.fixture
def context():
    class ContextCodec(BaseCodec):
        pass

    class ContextListCodec(BaseListCodec):
        pass

    codec = MagicMock(spec=ContextCodec)
    list_codec = MagicMock(spec=ContextListCodec)
    inner_codec = MagicMock()
    list_codec.get_inner_codec = lambda: inner_codec

    class Example:
        x = Field(codec, "x")
        y = Field(list_codec, "y")

        def __init__(self):
            self.x = None

    return Context(
        class_type=Example,
        codec=codec,
        list_codec=list_codec,
        list_inner_codec=inner_codec,
    )


def test_validate_called_on_set(context: Context) -> None:
    obj = context.class_type()
    obj.x = 123

    context.codec.validate.assert_called_with(123)
    assert obj.__dict__["x"] == 123


def test_list_validate_called_on_set(context: Context) -> None:
    obj = context.class_type()

    obj.y = [0, 1, 2]
    context.list_codec.validate.assert_called_once_with([0, 1, 2])

    obj.y[1] = 3
    context.list_inner_codec.validate.assert_called_with(3)


def test_get_after_set(context: Context) -> None:
    obj = context.class_type()

    obj.x = 456
    assert obj.x == 456


def test_list_get_after_set(context: Context) -> None:
    obj = context.class_type()

    obj.y = [1, 2, 3]

    obj.y[0] = 4

    assert obj.y[0] == 4


def test_get_on_class_raises_error(context: Context) -> None:
    with pytest.raises(UninitializedAccessError):
        _ = context.class_type.x  # type: ignore
