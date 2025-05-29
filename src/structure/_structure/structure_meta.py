from typing import Callable, Dict, get_origin, get_args, Annotated

from structure.codecs.base_codec import BaseCodec
from structure._structure.types import Fields
from structure._structure.method_creators import (
    _create_init,
    _create_repr,
    _create_dump,
    _create_parse,
)

ANNOTATIONS_KEY: str = "__annotations__"
METHOD_CREATORS: Dict[str, Callable[[Fields], Callable]] = {
    "__init__": _create_init,
    "__repr__": _create_repr,
    "dump": _create_dump,
    "parse": _create_parse,
}


class StructureMeta(type):
    def __new__(mcs, name, bases, namespace):
        annotations = namespace.get(ANNOTATIONS_KEY, {})
        fields = _construct_fields(annotations)

        for method_name, method_creator in METHOD_CREATORS.items():
            namespace[method_name] = method_creator(fields)

        return super().__new__(mcs, name, bases, namespace)


def _construct_fields(annotations: Dict[str, type]) -> Fields:
    fields: Fields = {}

    for field_name, annotated_type in annotations.items():
        origin = get_origin(annotated_type)
        args = get_args(annotated_type)

        if origin is not Annotated:
            raise RuntimeError("All structure fields must be `typing.Annotated`")

        if len(args) != 2:
            raise RuntimeError(
                "All Structure fields must be of the form `typing.Annotated[<base_type>, <structure_class_instance>]`"
            )

        base_type, codec = args

        if base_type != int or not isinstance(codec, BaseCodec):
            raise RuntimeError(
                "All structure fields must be in the form `typing.Annotated[int, Number(...)]`"
            )

        fields[field_name] = codec

    return fields
