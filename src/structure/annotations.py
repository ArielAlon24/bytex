from typing import Any, List, Optional, Tuple, get_args, get_origin, Annotated
import collections.abc

from structure.codecs.base_codec import BaseCodec
from structure.errors import StructureError

ANNOTATED_ARGS_COUNT: int = 2


def extract_type_and_codec(annotation: Any) -> Tuple[Any, BaseCodec]:
    if not get_origin(annotation) is Annotated:
        raise StructureError(
            "Invalid Annotated usage: expected `Annotated[Type, BaseCodec]`"
        )

    annotated_args = get_args(annotation)

    if len(annotated_args) != ANNOTATED_ARGS_COUNT:
        raise StructureError(
            "Invalid Annotated usage: expected `Annotated[Type, BaseCodec]`"
        )

    base_type, codec = annotated_args

    if not isinstance(codec, BaseCodec):
        raise StructureError(
            "Invalid Annotated usage: expected `Annotated[Type, BaseCodec]`"
        )

    return base_type, codec


def is_sequence_type(annotation: type) -> bool:
    origin = get_origin(annotation)
    if origin is None:
        return issubclass(annotation, collections.abc.Sequence)
    return issubclass(origin, collections.abc.Sequence)


def is_list_type(annotation: type) -> bool:
    return get_origin(annotation) is list or get_origin(annotation) is List


def get_list_type(annotation: type) -> Optional[type]:
    args = get_args(annotation)
    if args:
        return args[0]

    return None
