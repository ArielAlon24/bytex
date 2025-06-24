from typing import Any

from structure.annotations import extract_type_and_codec
from structure.codecs import IntegerCodec
from structure.length_encodings.base_length_encoding import BaseLengthEncoding
from structure.errors import StructureCreationError


class Prefix(BaseLengthEncoding):
    def __init__(self, size: Any) -> None:
        base_type, codec = extract_type_and_codec(size)

        if not base_type == int or not isinstance(codec, IntegerCodec):
            raise StructureCreationError(
                "Invalid Annotated usage: expected `Annotated[int, IntegerCodec]`"
            )

        self.codec = codec
