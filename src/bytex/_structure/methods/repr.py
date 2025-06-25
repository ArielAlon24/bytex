from typing import Callable

from bytex._structure.types import Codecs


def _create_repr(codecs: Codecs) -> Callable[[object], str]:
    def __repr__(self) -> str:
        result = f"{self.__class__.__name__}("

        for index, (name, codec) in enumerate(codecs.items()):
            value = getattr(self, name)

            if index == 0:
                result += f"{name}={repr(value)}"
            else:
                result += f", {name}={repr(value)}"

        return f"{result})"

    return __repr__
