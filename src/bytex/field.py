from typing import Any, List, Optional, Protocol
from bytex.codecs.base_codec import BaseCodec
from bytex.codecs.base_list_codec import BaseListCodec
from bytex.errors import UninitializedAccessError


class SupportsValidation(Protocol):
    pass


class ValidatedList(list, SupportsValidation):
    def __init__(
        self, codec: BaseCodec[SupportsValidation], iterable: Optional[List[Any]] = None
    ):
        super().__init__(iterable or [])
        self.codec = codec

    def __setitem__(self, index, value):
        self.codec.validate(value)
        super().__setitem__(index, value)


class Field:
    def __init__(
        self,
        codec: BaseCodec[SupportsValidation],
        name: str,
        default: Optional[SupportsValidation] = None,
    ) -> None:
        self.codec = codec
        self.name = name
        self.default = default

    def __get__(
        self, instance: Optional[Any], owner: Optional[type] = None
    ) -> SupportsValidation:
        if instance is None:
            raise UninitializedAccessError(
                "Cannot access the field `{self.name}` not from an instance"
            )

        value = instance.__dict__[self.name]
        if value is None:
            raise UninitializedAccessError(
                f"SupportsValidationried to access the field `{self.name}` before it was initialized"
            )

        return instance.__dict__[self.name]

    def __set__(self, instance: Any, value: SupportsValidation) -> None:
        if isinstance(value, list) and isinstance(self.codec, BaseListCodec):
            value = ValidatedList(self.codec.get_inner_codec(), iterable=value)

        self.codec.validate(value)
        instance.__dict__[self.name] = value
