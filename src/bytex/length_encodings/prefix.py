from typing import Any

from bytex.annotations import extract_type_and_value
from bytex.codecs import IntegerCodec
from bytex.errors import StructureCreationError
from bytex.length_encodings.base_length_encoding import BaseLengthEncoding


class Prefix(BaseLengthEncoding):
    def __init__(self, size: Any) -> None:
        base_type, codec = extract_type_and_value(size)

        if base_type is not int or not isinstance(codec, IntegerCodec):
            raise StructureCreationError(
                "Invalid Annotated usage: expected `Annotated[int, IntegerCodec]`"
            )

        self.codec = codec
