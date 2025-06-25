import pytest
from unittest.mock import MagicMock
from bytex.errors import UninitializedAccessError
from bytex.field import Field


@pytest.fixture
def fixture_class():
    codec = MagicMock()
    codec.validate = MagicMock()

    class Example:
        x = Field(codec, "x")

        def __init__(self):
            self.x = None

    return Example, codec


def test_validate_called_on_set(fixture_class):
    Example, codec = fixture_class
    obj = Example()

    obj.x = 123

    codec.validate.assert_called_with(123)
    assert obj.__dict__["x"] == 123


def test_get_after_set_returns_value(fixture_class):
    Example, _ = fixture_class
    obj = Example()

    obj.x = 456
    assert obj.x == 456


def test_get_on_class_raises_error(fixture_class):
    Example, _ = fixture_class

    with pytest.raises(UninitializedAccessError):
        _ = Example.x
