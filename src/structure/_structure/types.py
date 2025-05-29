from typing_extensions import TypeAlias
from typing import Dict

from structure.codecs.base_codec import BaseCodec

Fields: TypeAlias = Dict[str, BaseCodec]
