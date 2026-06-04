"""Extensible STIX parsing support."""

from metamodel.io.stix.constants import (
    STIX_DOMAIN_OBJECT_TYPES,
    STIX_RELATIONSHIP_OBJECT_TYPES,
    STIX_CYBER_OBSERVABLE_OBJECT_TYPES,
    STIX_META_OBJECT_TYPES,
    STIX_STANDARD_TYPES,
)
from metamodel.io.stix.generic import GenericStixObject, GenericStixRelationship
from metamodel.io.stix.registry import (
    StixObjectMapperRegistry,
    StixRelationshipMapperRegistry,
    StixParserContext,
)
from metamodel.io.stix.mappers import (
    build_default_object_registry,
    build_default_relationship_registry,
)

__all__ = [
    "STIX_DOMAIN_OBJECT_TYPES",
    "STIX_RELATIONSHIP_OBJECT_TYPES",
    "STIX_CYBER_OBSERVABLE_OBJECT_TYPES",
    "STIX_META_OBJECT_TYPES",
    "STIX_STANDARD_TYPES",
    "GenericStixObject",
    "GenericStixRelationship",
    "StixObjectMapperRegistry",
    "StixRelationshipMapperRegistry",
    "StixParserContext",
    "build_default_object_registry",
    "build_default_relationship_registry",
]
