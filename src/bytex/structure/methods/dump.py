from typing import Callable

from bytex.bits import BitBuffer
from bytex.endianes import Endianes
from bytex.errors import AlignmentError
from bytex.structure.types import Fields


def _create_dump(fields: Fields) -> Callable[[object, Endianes], bytes]:
    def dump(self, endianes: Endianes = Endianes.LITTLE) -> bytes:
        buffer = BitBuffer()
        for name, field in fields.items():
            value = getattr(self, name)
            buffer.write(field.codec.serialize(value, endianes=endianes))

        try:
            return buffer.to_bytes()
        except AlignmentError as e:
            raise AlignmentError(
                "Cannot dump a structure whose bit size is not a multiple of 8"
            ) from e

    return dump
