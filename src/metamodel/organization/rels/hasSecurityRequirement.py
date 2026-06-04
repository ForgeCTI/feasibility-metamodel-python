from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.Asset import Asset
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement


class hasSecurityRequirement(BaseRelationship):
    """Connects Asset to AssetSecurityRequirement."""

    source_type = Asset
    target_type = AssetSecurityRequirement
    source_cardinality = '1'
    target_cardinality = '1..*'
