from typing import Dict, TYPE_CHECKING

from bytex.codecs.base_codec import BaseCodec


# Use `typing_extensions` only in `TYPE_CHECKING` mode to not require the `typing_extensions` module

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

    Codecs: TypeAlias = Dict[str, BaseCodec]
else:
    Codecs = Dict[str, BaseCodec]
