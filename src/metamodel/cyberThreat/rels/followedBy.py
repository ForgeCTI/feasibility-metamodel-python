from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep


class followedBy(BaseRelationship):
    """ThreatStep --followedBy--> ThreatStep."""

    label = 'followedBy'
    source_type = ThreatStep
    target_type = ThreatStep
    source_cardinality = '0..*'
    target_cardinality = '0..*'
