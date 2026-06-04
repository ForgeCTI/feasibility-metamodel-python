from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Threat import Threat


class initiates(BaseRelationship):
    """Connects ThreatActor to Threat."""

    source_type = ThreatActor
    target_type = Threat
    source_cardinality = '1'
    target_cardinality = '1'
