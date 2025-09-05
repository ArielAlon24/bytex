from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bytex.bits import Bits, BitBuffer
from bytex.endianes import Endianes


T = TypeVar("T")


class BaseCodec(ABC, Generic[T]):

    @abstractmethod
    def serialize(self, value: T, endianes: Endianes) -> Bits:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, bit_buffer: BitBuffer, endianes: Endianes) -> T:
        raise NotImplementedError

    @abstractmethod
    def validate(self, value: T) -> None:
        raise NotImplementedError
