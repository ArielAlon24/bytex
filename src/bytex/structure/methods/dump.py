from typing import Callable

from bytex.structure.types import Fields
from bytex.endianes import Endianes
from bytex.bits import BitBuffer
from bytex.errors import AlignmentError


def _create_dump(fields: Fields) -> Callable[[object, Endianes], bytes]:
    def dump(self, endianes: Endianes = Endianes.LITTLE) -> bytes:
        buffer = BitBuffer()
        for name, field in fields.items():
            value = getattr(self, name)
            buffer.write(field.codec.serialize(value))

        try:
            return buffer.to_bytes(endianes=endianes)
        except AlignmentError as e:
            raise AlignmentError(
                "Cannot dump a structure whose bit size is not a multiple of 8"
            ) from e

    return dump
