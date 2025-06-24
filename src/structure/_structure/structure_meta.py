from typing import Callable, Dict, List, Optional, get_origin, get_args, Annotated
import collections.abc

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
from structure.length_encodings import BaseLengthEncoding, Terminator, Fixed
from structure.codecs import (
    BaseCodec,
    StructureCodec,
    DataCodec,
    TerminatedListCodec,
    TerminatedStringCodec,
    TerminatedBytesCodec,
    FixedStringCodec,
    FixedBytesCodec,
)


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
            "All Structure fields must be of the form `typing.Annotated[Any, BaseCodec(...)]` or "
            "typing.Annotated[Sequence, BaseLengthEncoding(...)]"
        )

    base_type, value = args

    if isinstance(value, BaseCodec):
        return value
    if isinstance(value, BaseLengthEncoding):
        return _construct_length_encoded_codec(
            base_type=base_type, length_encoding=value
        )

    raise StructureCreationError(
        "All Structure fields must be of the form `typing.Annotated[Any, BaseCodec(...)]` or "
        "typing.Annotated[Sequence, BaseLengthEncoding(...)]"
    )


def _construct_length_encoded_codec(
    base_type: type, length_encoding: BaseLengthEncoding
) -> BaseCodec:
    if not _is_sequence_type(base_type):
        raise StructureCreationError(
            f"Only `Sequence` types can have a length encoding, got: `{str(base_type)}`"
        )

    if base_type == str:
        return _construct_str_length_encoded_codec(length_encoding)
    elif base_type == bytes:
        return _construct_bytes_length_encoded_codec(length_encoding)
    elif _is_list_type(base_type):
        return _construct_list_length_encoded_codec(base_type, length_encoding)

    raise StructureCreationError(
        f"Could not create a length encoded codec, Unimplemented length encoded type: {base_type}"
    )


def _construct_str_length_encoded_codec(
    length_encoding: BaseLengthEncoding,
) -> BaseCodec:
    if isinstance(length_encoding, Terminator):
        return TerminatedStringCodec(length_encoding.get_terminator())
    if isinstance(length_encoding, Fixed):
        return FixedStringCodec(length=length_encoding.length)
    raise StructureCreationError(
        f"Unsupported length encoding ('{length_encoding.__class__.__name__}') for `str`"
    )


def _construct_bytes_length_encoded_codec(
    length_encoding: BaseLengthEncoding,
) -> BaseCodec:
    if isinstance(length_encoding, Terminator):
        return TerminatedBytesCodec(length_encoding.get_terminator())
    if isinstance(length_encoding, Fixed):
        return FixedBytesCodec(length_encoding.length)
    raise StructureCreationError(
        f"Unsupported length encoding ('{length_encoding.__class__.__name__}') for `bytes`"
    )


def _construct_list_length_encoded_codec(
    base_type: type, length_encoding: BaseLengthEncoding
) -> BaseCodec:
    list_item_type = _get_list_type(base_type)
    if list_item_type is None:
        raise StructureCreationError(
            "All list types must include the item type - `List[ItemType]`, got a list without an item type"
        )

    item_codec = _resolve_list_item_codec(list_item_type)

    if isinstance(length_encoding, Terminator):
        return TerminatedListCodec(
            item_codec=item_codec, terminator=length_encoding.get_terminator()
        )

    raise StructureCreationError("Unsupported length encoding for `List[...]`.")


def _resolve_list_item_codec(list_item_type: type) -> BaseCodec:
    if get_origin(list_item_type) is Annotated:
        annotated_args = get_args(list_item_type)

        if len(annotated_args) >= 2 and isinstance(annotated_args[1], BaseCodec):
            return annotated_args[1]

        raise StructureCreationError(
            "Invalid Annotated usage: expected `Annotated[Type, BaseCodec]`"
        )

    if issubclass(list_item_type, _Structure):
        return StructureCodec(structure_class=list_item_type)

    raise StructureCreationError(
        "List item types must be either a `Structure` subclass or `Annotated[_, BaseCodec]`"
    )


def _is_sequence_type(annotation: type) -> bool:
    origin = get_origin(annotation)
    if origin is None:
        return issubclass(annotation, collections.abc.Sequence)
    return issubclass(origin, collections.abc.Sequence)


def _is_list_type(annotation: type) -> bool:
    return get_origin(annotation) is list or get_origin(annotation) is List


def _get_list_type(annotation: type) -> Optional[type]:
    args = get_args(annotation)
    if args:
        return args[0]

    return None


def _validate_codecs(codecs: Codecs) -> None:
    if len(codecs) == 0:
        return

    for codec, _ in zip(codecs.values(), range(0, len(codecs) - 1)):
        if isinstance(codec, DataCodec):
            raise StructureCreationError(
                f"A field with codec `{DataCodec.__name__}` must singular and come last"
            )
