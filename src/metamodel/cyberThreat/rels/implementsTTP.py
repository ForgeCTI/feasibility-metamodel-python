from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep


class implementsTTP(BaseRelationship):
    """ThreatStep --implements--> TTP."""

    label = 'implements'
    source_type = ThreatStep
    target_type = TTP
    source_cardinality = '0..*'
    target_cardinality = '1'
