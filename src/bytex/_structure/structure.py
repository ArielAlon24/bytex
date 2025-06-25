from bytex._structure.structure_meta import StructureMeta
from bytex._structure._structure import _Structure


class Structure(_Structure, metaclass=StructureMeta):
    pass
