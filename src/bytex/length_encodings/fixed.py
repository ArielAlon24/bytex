from dataclasses import dataclass

from bytex.length_encodings.base_length_encoding import BaseLengthEncoding
from bytex.errors import StructureCreationError


@dataclass
class Fixed(BaseLengthEncoding):
    length: int

    def __post_init__(self) -> None:
        if self.length < 0:
            raise StructureCreationError(
                f"The {self.__class__.__name__} length encoding must have a positive `length`, got: '{self.length}'"
            )
