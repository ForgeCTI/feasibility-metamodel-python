class MetamodelError(Exception):
    """Base exception for metamodel errors."""


class ValidationError(MetamodelError):
    """Raised when validation fails in strict mode."""


class RegistryError(MetamodelError):
    """Raised when an entity or relationship type cannot be resolved."""


class ParseError(MetamodelError):
    """Raised when a scenario file or mapping cannot be converted into a Model."""
