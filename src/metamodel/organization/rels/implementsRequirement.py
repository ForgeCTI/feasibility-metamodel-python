from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement


class implementsRequirement(BaseRelationship):
    """Connects AssetSecurityRequirement to SecurityRequirement."""

    source_type = AssetSecurityRequirement
    target_type = SecurityRequirement
    source_cardinality = '1..*'
    target_cardinality = '1'
