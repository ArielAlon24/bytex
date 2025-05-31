from structure._structure.structure_meta import StructureMeta
from structure._structure._structure import _Structure


class Structure(_Structure, metaclass=StructureMeta):
    pass
