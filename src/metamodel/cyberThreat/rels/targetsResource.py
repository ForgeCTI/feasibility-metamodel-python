from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.infrastructure.entities.Resource import Resource


class targetsResource(BaseRelationship):
    """Connects ThreatStep to Resource."""

    source_type = ThreatStep
    target_type = Resource
    source_cardinality = '1..*'
    target_cardinality = '1'
