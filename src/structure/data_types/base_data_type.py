from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from structure.codecs.base_codec import BaseCodec

T = TypeVar("T")


class BaseDataType(ABC, Generic[T]):
    _codec: BaseCodec[int]

    @abstractmethod
    def __new__(cls, codec: BaseCodec[T], value: T) -> object:
        raise NotImplementedError

    @abstractmethod
    def _raw(self) -> T:
        raise NotImplementedError
