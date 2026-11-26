from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor


class initiates(BaseRelationship):
    """ThreatActor --initiates--> Threat."""

    label = 'initiates'
    source_type = ThreatActor
    target_type = Threat
    source_cardinality = '1'
    target_cardinality = '1..*'
