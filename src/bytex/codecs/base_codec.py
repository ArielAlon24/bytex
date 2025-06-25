from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bytex.bits import Bits, BitBuffer


T = TypeVar("T")


class BaseCodec(ABC, Generic[T]):

    @abstractmethod
    def serialize(self, value: T) -> Bits:
        raise NotImplementedError

    @abstractmethod
    def deserialize(self, bit_buffer: BitBuffer) -> T:
        raise NotImplementedError

    @abstractmethod
    def validate(self, value: T) -> None:
        raise NotImplementedError
