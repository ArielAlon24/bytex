from typing import Annotated, Any, get_args, get_origin

from structure.codecs import IntegerCodec
from structure.length_encodings.base_length_encoding import BaseLengthEncoding
from structure.errors import StructureCreationError


class Prefix(BaseLengthEncoding):
    def __init__(self, size: Any) -> None:
        if not get_origin(size) is Annotated:
            raise StructureCreationError(
                "1 Invalid Annotated usage: expected `Annotated[int, IntegerCodec]`"
            )

        annotated_args = get_args(size)

        if len(annotated_args) != 2:
            raise StructureCreationError(
                "2 Invalid Annotated usage: expected `Annotated[int, IntegerCodec]`"
            )

        base_type, codec = annotated_args

        if not base_type == int or not isinstance(codec, IntegerCodec):
            raise StructureCreationError(
                "3 Invalid Annotated usage: expected `Annotated[int, IntegerCodec]`"
            )

        self.codec = codec
