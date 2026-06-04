from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.TTP import TTP


class implementsTTP(BaseRelationship):
    """Connects ThreatStep to TTP."""

    source_type = ThreatStep
    target_type = TTP
    source_cardinality = '1..*'
    target_cardinality = '1'
