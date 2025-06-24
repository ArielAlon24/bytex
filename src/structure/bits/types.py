from typing import List, TYPE_CHECKING

# Use `typing_extensions` only in `TYPE_CHECKING` mode to not require the `typing_extensions` module

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    Bits: TypeAlias = List[bool]
else:
    Bits = List[bool]
