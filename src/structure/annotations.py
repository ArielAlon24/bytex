from typing import Any, get_args, get_origin, Annotated

from structure.codecs.base_codec import BaseCodec
from structure.errors import StructureCreationError


def extract_codec(annotation: Any) -> BaseCodec:
    if not get_origin(annotation) is Annotated:
        raise StructureCreationError(
            "Invalid Annotated usage: expected `Annotated[Type, BaseCodec]`"
        )

    annotated_args = get_args(annotation)

    if len(annotated_args) >= 2 and isinstance(annotated_args[1], BaseCodec):
        return annotated_args[1]

    raise StructureCreationError(
        "Invalid Annotated usage: expected `Annotated[Type, BaseCodec]`"
    )
