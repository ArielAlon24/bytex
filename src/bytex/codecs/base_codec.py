from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bytex.bits import BitBuffer, Bits
from bytex.endianness import Endianness

T = TypeVar("T")


class BaseCodec(ABC, Generic[T]):

    @abstractmethod
    def serialize(self, value: T, endianness: Endianness) -> Bits:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, bit_buffer: BitBuffer, endianness: Endianness) -> T:
        raise NotImplementedError

    @abstractmethod
    def validate(self, value: T) -> None:
        raise NotImplementedError
