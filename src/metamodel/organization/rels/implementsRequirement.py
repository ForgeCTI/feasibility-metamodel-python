from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement


class implementsRequirement(BaseRelationship):
    """AssetSecurityRequirement --implementationOf--> SecurityRequirement."""

    label = 'implementationOf'
    source_type = AssetSecurityRequirement
    target_type = SecurityRequirement
    source_cardinality = '0..*'
    target_cardinality = '1'
