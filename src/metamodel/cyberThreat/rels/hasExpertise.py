from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Expertise import Expertise
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor


class hasExpertise(BaseRelationship):
    """ThreatActor --hasExpertise--> Expertise."""

    label = 'hasExpertise'
    source_type = ThreatActor
    target_type = Expertise
    source_cardinality = '0..*'
    target_cardinality = '0..1'
