from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.BusinessRequirement import BusinessRequirement
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement


class drivesSecurityRequirement(BaseRelationship):
    """Connects BusinessRequirement to AssetSecurityRequirement."""

    source_type = BusinessRequirement
    target_type = AssetSecurityRequirement
    source_cardinality = '1..*'
    target_cardinality = '1..*'
