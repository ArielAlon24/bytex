from typing import TYPE_CHECKING, List

# Use `typing_extensions` only in `TYPE_CHECKING` mode to not require the `typing_extensions` module

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    Bits: TypeAlias = List[bool]
else:
    Bits = List[bool]
