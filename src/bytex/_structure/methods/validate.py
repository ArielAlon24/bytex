from typing import Callable

from bytex._structure.types import Codecs


def _create_validate(codecs: Codecs) -> Callable[[object], None]:
    def validate(self) -> None:
        for name, codec in codecs.items():
            value = getattr(self, name)
            codec.validate(value)

    return validate
