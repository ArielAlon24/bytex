from typing import Callable

from bytex.structure.types import Fields


def _create_repr(fields: Fields) -> Callable[[object], str]:
    def __repr__(self) -> str:
        result = f"{self.__class__.__name__}("

        for index, (name, field) in enumerate(fields.items()):
            value = getattr(self, name)

            if index == 0:
                result += f"{name}={repr(value)}"
            else:
                result += f", {name}={repr(value)}"

        return f"{result})"

    return __repr__
