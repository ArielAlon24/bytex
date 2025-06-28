from typing import Any, Optional, TypeVar, Generic
from bytex.codecs.base_codec import BaseCodec
from bytex.errors import UninitializedAccessError

T = TypeVar("T")


class Field(Generic[T]):
    def __init__(
        self, codec: BaseCodec[T], name: str, default: Optional[T] = None
    ) -> None:
        self.codec = codec
        self.name = name
        self.default = default

    def __get__(self, instance: Optional[Any], owner: Optional[type] = None) -> T:
        if instance is None:
            raise UninitializedAccessError(
                "Cannot access the field `{self.name}` not from an instance"
            )

        value = instance.__dict__[self.name]
        if value is None:
            raise UninitializedAccessError(
                f"Tried to access the field `{self.name}` before it was initialized"
            )

        return instance.__dict__[self.name]

    def __set__(self, instance: Any, value: T) -> None:
        self.codec.validate(value)
        instance.__dict__[self.name] = value
