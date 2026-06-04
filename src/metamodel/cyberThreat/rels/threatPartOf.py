from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.Campaign import Campaign


class threatPartOf(BaseRelationship):
    """Connects Threat to Campaign."""

    source_type = Threat
    target_type = Campaign
    source_cardinality = '1..*'
    target_cardinality = '1'
