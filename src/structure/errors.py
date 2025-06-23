class StructureError(Exception):
    pass


class StructureCreationError(Exception):
    pass


class ValidationError(StructureError):
    pass


class AlignmentError(StructureError):
    pass


class InsufficientDataError(StructureError):
    pass


class ParsingError(StructureError):
    pass


class UninitializedAccessError(StructureError):
    pass
