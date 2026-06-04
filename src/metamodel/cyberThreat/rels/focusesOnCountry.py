from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.organization.entities.HomeCountry import HomeCountry


class focusesOnCountry(BaseRelationship):
    """Connects Campaign to HomeCountry."""

    source_type = Campaign
    target_type = HomeCountry
    source_cardinality = '0..*'
    target_cardinality = '0..*'
