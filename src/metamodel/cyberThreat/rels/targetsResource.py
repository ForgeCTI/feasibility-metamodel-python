from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep


class targetsResource(BaseRelationship):
    """ThreatStep --targetsResource--> Resource."""

    label = 'targetsResource'
    source_type = ThreatStep
    target_type = Resource
    source_cardinality = '0..*'
    target_cardinality = '0..*'
