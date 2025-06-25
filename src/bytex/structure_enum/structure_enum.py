from enum import Enum, EnumMeta
from types import MappingProxyType
from typing import Any, Type

from bytex.annotations import extract_type_and_value
from bytex.codecs.base_codec import BaseCodec
from bytex.errors import (
    StructureEnumCreationError,
    ValidationError,
)
from bytex.structure_enum._structure_enum import (
    _StructureEnum,
    STRUCTURE_ENUM_CODEC_KEY,
)


ENUM_VALUE_KEY: str = "value"


def StructureEnum(size: Any) -> Type[Enum]:
    _, codec = extract_type_and_value(annotation=size)
    if not isinstance(codec, BaseCodec):
        raise StructureEnumCreationError(
            "Invalid Annotated usage: expected `Annotated[type, BaseCodec]`"
        )

    class StructureEnumMeta(EnumMeta):
        def __new__(metacls, clsname, bases, clsdict, **kwargs):
            cls = super().__new__(metacls, clsname, bases, clsdict)

            if len(cls.__members__) == 0:
                return cls

            _validate_enum_members(codec=codec, members=cls.__members__)

            return cls

    class NewEnum(_StructureEnum, metaclass=StructureEnumMeta):
        pass

    setattr(NewEnum, STRUCTURE_ENUM_CODEC_KEY, codec)

    return NewEnum


def _validate_enum_members(codec: BaseCodec, members: MappingProxyType) -> None:
    for key, member in members.items():
        value = getattr(member, ENUM_VALUE_KEY)

        try:
            codec.validate(value)
        except ValidationError as e:
            raise StructureEnumCreationError(
                f"Could not create StructureEnum - invalid value {value} for member `{key}`"
            ) from e
