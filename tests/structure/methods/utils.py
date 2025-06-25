from dataclasses import dataclass
from typing import Dict, Generic, TypeVar

from bytex._structure.types import Codecs
from bytex.codecs.base_codec import BaseCodec
from bytex.field import Field

T = TypeVar("T")


@dataclass
class Value(Generic[T]):
    value: T
    codec: BaseCodec


Values = Dict[str, Value]


def _create_codecs(values: Values) -> Codecs:
    return {name: field.codec for name, field in values.items()}


def _create_instance(values: Values, name: str = "") -> object:
    instance = _create_type(values=values, name=name)()
    instance.__class__.__name__ = name

    for name, value in values.items():
        setattr(instance, name, value.value)

    return instance


def _create_type(values: Values, name: str = "") -> type:
    fields = {
        name: Field(codec=value.codec, name=name) for name, value in values.items()
    }
    return type(name, tuple(), fields)


def _create_empty_instance(name: str = "") -> object:
    return type(name, tuple(), {})()
