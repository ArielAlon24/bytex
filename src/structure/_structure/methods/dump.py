from typing import Callable

from structure._structure.types import Codecs
from structure.endianes import Endianes
from structure.bits import BitBuffer
from structure.errors import AlignmentError


def _create_dump(codecs: Codecs) -> Callable[[object, Endianes], bytes]:
    def dump(self, endianes: Endianes = Endianes.LITTLE) -> bytes:
        buffer = BitBuffer()
        for name, codec in codecs.items():
            value = getattr(self, name)
            buffer.write(codec.serialize(value))

        try:
            return buffer.to_bytes(endianes=endianes)
        except AlignmentError as e:
            raise AlignmentError(
                "Cannot dump a structure whose bit size is not a multiple of 8"
            ) from e

    return dump
