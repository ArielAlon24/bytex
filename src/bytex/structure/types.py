from typing import Dict, TYPE_CHECKING

from bytex.codecs.base_codec import BaseCodec
from bytex.field import Field


# Use `typing_extensions` only in `TYPE_CHECKING` mode to not require the `typing_extensions` module

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    Codecs: TypeAlias = Dict[str, BaseCodec]
    Fields: TypeAlias = Dict[str, Field]
else:
    Codecs = Dict[str, BaseCodec]
    Fields = Dict[str, Field]
