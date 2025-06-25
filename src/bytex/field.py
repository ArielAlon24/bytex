from typing import Any, Optional
from bytex.codecs.base_codec import BaseCodec
from bytex.errors import UninitializedAccessError


class Field:
    def __init__(self, codec: BaseCodec[int], name: str) -> None:
        self._codec = codec
        self._name = name

    def __get__(self, instance: Optional[Any], owner: Optional[type] = None) -> int:
        if instance is None:
            raise UninitializedAccessError(
                "Cannot access the field `{self._name}` not from an instance"
            )

        value = instance.__dict__[self._name]
        if value is None:
            raise UninitializedAccessError(
                f"Tried to access the field `{self._name}` before it was initialized"
            )

        return instance.__dict__[self._name]

    def __set__(self, instance: Any, value: Any) -> None:
        self._codec.validate(value)
        instance.__dict__[self._name] = value
