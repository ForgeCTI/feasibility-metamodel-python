from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep


class startsWith(BaseRelationship):
    """Connects Threat to ThreatStep."""

    source_type = Threat
    target_type = ThreatStep
    source_cardinality = '1'
    target_cardinality = '1'
