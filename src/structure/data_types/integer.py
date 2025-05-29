from __future__ import annotations

from typing import Any
from structure.codecs.base_codec import BaseCodec
from structure.data_types.base_data_type import BaseDataType
from structure.errors import ValidationError


class Integer(int, BaseDataType[int]):
    _codec: BaseCodec[int]

    def __new__(cls, codec: BaseCodec[int], value: int) -> Integer:
        codec.validate(value)
        instance = super().__new__(cls, value)
        instance._codec = codec
        return instance

    def _raw(self) -> int:
        return int(self)

    def __add__(self, other: Any) -> Integer:
        result = int.__add__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __sub__(self, other: Any) -> Integer:
        result = int.__sub__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __mul__(self, other: Any) -> Integer:
        result = int.__mul__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __floordiv__(self, other: Any) -> Integer:
        result = int.__floordiv__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __truediv__(self, other: Any) -> Integer:
        raise ValidationError(
            f"Cannot use `__truediv__` on an `{self.__class__.__name__}`. If this is intentional, cast the value into a float"
        )

    def __mod__(self, other: Any) -> Integer:
        result = int.__mod__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __pow__(self, other: Any, modulo=None):
        raise ValidationError(
            f"Cannot use `__truediv__` on an `{self.__class__.__name__}`. If this is operation is intentional, cast the value into a float."
        )

    def __neg__(self) -> Integer:
        result = int.__neg__(self)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __and__(self, other: Any) -> Integer:
        result = int.__and__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __or__(self, other: Any) -> Integer:
        result = int.__or__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __xor__(self, other: Any) -> Integer:
        result = int.__xor__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __lshift__(self, other: Any) -> Integer:
        result = int.__lshift__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)

    def __rshift__(self, other: Any) -> Integer:
        result = int.__rshift__(self, other)
        self._codec.validate(result)
        return Integer(self._codec, result)
