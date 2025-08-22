from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from bytex.codecs.base_codec import BaseCodec

T = TypeVar("T")


class BaseListCodec(BaseCodec, ABC, Generic[T]):

    @abstractmethod
    def get_inner_codec(self) -> BaseCodec:
        raise NotImplementedError
