from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Adversary import Adversary
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor


class relatedTo(BaseRelationship):
    """ThreatActor --relatedTo--> Adversary."""

    label = 'relatedTo'
    source_type = ThreatActor
    target_type = Adversary
    source_cardinality = '1..*'
    target_cardinality = '0..*'
