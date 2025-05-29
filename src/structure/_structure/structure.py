from __future__ import annotations

from typing import Any
from typing_extensions import Self
from structure._structure.structure_meta import StructureMeta
from structure.endianes import Endianes


class Structure(metaclass=StructureMeta):
    def __init__(self, **data: Any) -> None:
        raise NotImplementedError

    def dump(self, endianes: Endianes = Endianes.LITTLE) -> bytes:
        raise NotImplementedError

    @classmethod
    def parse(cls, data: bytes, endianes: Endianes = Endianes.LITTLE) -> Self:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
