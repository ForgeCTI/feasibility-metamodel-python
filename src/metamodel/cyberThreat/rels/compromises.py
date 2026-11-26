from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep


class compromises(BaseRelationship):
    """ThreatStep --compromises--> AssetSecurityRequirement."""

    label = 'compromises'
    source_type = ThreatStep
    target_type = AssetSecurityRequirement
    source_cardinality = '0..*'
    target_cardinality = '0..*'
