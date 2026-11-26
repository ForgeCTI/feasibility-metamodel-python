from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.organization.entities.Sector import Sector


class targetsSector(BaseRelationship):
    """Campaign --focusesOn--> Sector."""

    label = 'focusesOn'
    source_type = Campaign
    target_type = Sector
    source_cardinality = '0..*'
    target_cardinality = '0..*'
