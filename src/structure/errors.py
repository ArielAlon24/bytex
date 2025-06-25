class StructureError(Exception):
    pass


class StructureCreationError(Exception):
    pass


class StructureEnumCreationError(StructureCreationError):
    pass


class ValidationError(StructureError):
    pass


class AlignmentError(StructureError):
    pass


class ParsingError(StructureError):
    pass


class InsufficientDataError(ParsingError):
    pass


class UninitializedAccessError(StructureError):
    pass
