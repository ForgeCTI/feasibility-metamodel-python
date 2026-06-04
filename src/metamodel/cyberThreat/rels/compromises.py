from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement


class compromises(BaseRelationship):
    """Connects ThreatStep to AssetSecurityRequirement."""

    source_type = ThreatStep
    target_type = AssetSecurityRequirement
    source_cardinality = '1..*'
    target_cardinality = '1'
