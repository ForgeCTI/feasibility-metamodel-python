from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor


class aliasOf(BaseRelationship):
    """ThreatActor --alias--> ThreatActor."""

    label = 'alias'
    source_type = ThreatActor
    target_type = ThreatActor
    source_cardinality = '0..*'
    target_cardinality = '0..*'
