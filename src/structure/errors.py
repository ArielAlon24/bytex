class StructureError(Exception):
    pass


class ValidationError(StructureError):
    pass


class AlignmentError(StructureError):
    pass


class InsufficientDataError(StructureError):
    pass


class ParsingError(StructureError):
    pass
