from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor


class aliasOf(BaseRelationship):
    """Connects ThreatActor to ThreatActor."""

    source_type = ThreatActor
    target_type = ThreatActor
    source_cardinality = '0..*'
    target_cardinality = None
