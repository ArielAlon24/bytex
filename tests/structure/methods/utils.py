from typing import Dict

from structure.data_types.base_data_type import BaseDataType
from structure._structure.types import Fields

Values = Dict[str, BaseDataType]


def _create_fields(values: Values) -> Fields:
    return {name: field._codec for name, field in values.items()}


def _create_instance(values: Values, name: str = "") -> object:
    instance = _create_type(values=values, name=name)()
    instance.__class__.__name__ = name

    return instance


def _create_type(values: Values, name: str = "") -> type:
    return type(name, tuple(), values)


def _create_empty_instance(name: str = "") -> object:
    return type(name, tuple(), {})()
