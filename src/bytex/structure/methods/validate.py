from typing import Callable

from bytex.structure.types import Fields


def _create_validate(fields: Fields) -> Callable[[object], None]:
    def validate(self) -> None:
        for name, field in fields.items():
            value = getattr(self, name)
            field.codec.validate(value)

    return validate
