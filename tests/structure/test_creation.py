import typing
from pathlib import Path

import pytest

from bytex import Structure
from bytex.errors import StructureCreationError
from bytex.types import U8, Data


def test_create_structure_invalid_types1() -> None:
    with pytest.raises(StructureCreationError):

        class A(Structure):
            a: int


def test_create_structure_invalid_types2() -> None:
    with pytest.raises(StructureCreationError):

        class A(Structure):
            a: typing.Annotated[int, Path("/tmp")]


def test_create_structure_data_non_last_fails() -> None:
    with pytest.raises(StructureCreationError):

        class A(Structure):
            data: Data
            a: U8


def test_create_structure_data_last_succeeds() -> None:
    class A(Structure):
        a: U8
        data: Data
