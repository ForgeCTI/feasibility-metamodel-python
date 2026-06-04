from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Campaign import Campaign
from metamodel.organization.entities.InternationalBody import InternationalBody


class targetsInternationalBody(BaseRelationship):
    """Connects Campaign to InternationalBody."""

    source_type = Campaign
    target_type = InternationalBody
    source_cardinality = '0..*'
    target_cardinality = '0..*'
