import pytest

from bytex import BitBuffer
from bytex.codecs import FlagCodec
from bytex.errors import ValidationError


@pytest.mark.parametrize("value", [True, False])
def test_flag_validate_success(value: bool):
    codec = FlagCodec()
    codec.validate(value)


@pytest.mark.parametrize("value", [None, 0, 1, "true", [], {}])
def test_flag_validate_failure(value):
    codec = FlagCodec()
    with pytest.raises(ValidationError):
        codec.validate(value)


@pytest.mark.parametrize("value, expected_bits", [(True, [True]), (False, [False])])
def test_flag_serialize(value: bool, expected_bits):
    codec = FlagCodec()
    bits = codec.serialize(value)
    assert bits == expected_bits


@pytest.mark.parametrize("bits, expected_value", [([True], True), ([False], False)])
def test_flag_deserialize(bits, expected_value):
    codec = FlagCodec()
    buffer = BitBuffer()
    buffer.write(bits)
    result = codec.deserialize(buffer)
    assert result is expected_value


@pytest.mark.parametrize("value", [True, False])
def test_flag_serialize_deserialize_roundtrip(value: bool):
    codec = FlagCodec()
    bits = codec.serialize(value)
    buffer = BitBuffer()
    buffer.write(bits)
    result = codec.deserialize(buffer)
    assert result is value
