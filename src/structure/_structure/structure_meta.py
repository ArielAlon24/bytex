from typing import Callable, Dict, get_origin, get_args, Annotated

from structure.codecs import BaseCodec, StructureCodec, DataCodec
from structure._structure._structure import _Structure
from structure._structure.types import Codecs
from structure._structure.method_creators import (
    _create_init,
    _create_dump,
    _create_dump_bits,
    _create_parse,
    _create_parse_bits,
    _create_validate,
    _create_repr,
)
from structure.errors import StructureCreationError

ANNOTATIONS_KEY: str = "__annotations__"
METHOD_CREATORS: Dict[str, Callable[[Codecs], Callable]] = {
    "__init__": _create_init,
    "dump": _create_dump,
    "dump_bits": _create_dump_bits,
    "parse": _create_parse,
    "parse_bits": _create_parse_bits,
    "validate": _create_validate,
    "__repr__": _create_repr,
}


class StructureMeta(type):
    def __new__(mcs, name, bases, namespace):
        annotations = namespace.get(ANNOTATIONS_KEY, {})
        codecs = _construct_codecs(annotations)
        _validate_codecs(codecs)

        for method_name, method_creator in METHOD_CREATORS.items():
            namespace[method_name] = method_creator(codecs)

        return super().__new__(mcs, name, bases, namespace)


def _construct_codecs(annotations: Dict[str, type]) -> Codecs:
    codecs: Codecs = {}

    for field_name, annotation in annotations.items():
        codecs[field_name] = _construct_codec(annotation)

    return codecs


def _construct_codec(annotation: type) -> BaseCodec:
    if isinstance(annotation, type) and issubclass(annotation, _Structure):
        return StructureCodec(structure_class=annotation)

    origin = get_origin(annotation)
    args = get_args(annotation)

    if origin is not Annotated:
        raise StructureCreationError(
            "All structure fields must be of type `typing.Annotated`"
        )

    if len(args) != 2:
        raise StructureCreationError(
            "All Structure fields must be of the form `typing.Annotated[Any, BaseCodec(...)]`"
        )

    base_type, codec = args

    if not isinstance(codec, BaseCodec):
        raise StructureCreationError(
            "All structure fields must be in the form `typing.Annotated[Any, BaseCodec(...)]`"
        )

    return codec


def _validate_codecs(codecs: Codecs) -> None:
    if len(codecs) == 0:
        return

    for codec, _ in zip(codecs.values(), range(0, len(codecs) - 1)):
        if isinstance(codec, DataCodec):
            raise StructureCreationError(
                f"A field with codec `{DataCodec.__name__}` must singular and come last"
            )
