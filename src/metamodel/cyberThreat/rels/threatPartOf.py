from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.cyberThreat.entities.Threat import Threat


class threatPartOf(BaseRelationship):
    """Threat --partOf--> Campaign."""

    label = 'partOf'
    source_type = Threat
    target_type = Campaign
    source_cardinality = '1..*'
    target_cardinality = '0..1'
