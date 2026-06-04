class MetamodelError(Exception):
    """Base exception for metamodel errors."""


class ValidationError(MetamodelError):
    """Raised when validation fails in strict mode."""


class RegistryError(MetamodelError):
    """Raised when an entity or relationship type cannot be resolved."""


class TaxonomyError(MetamodelError):
    """Raised when taxonomy references cannot be resolved."""
