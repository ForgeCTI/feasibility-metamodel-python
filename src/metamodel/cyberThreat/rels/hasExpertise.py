from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Expertise import Expertise


class hasExpertise(BaseRelationship):
    """Connects ThreatActor to Expertise."""

    source_type = ThreatActor
    target_type = Expertise
    source_cardinality = '1..*'
    target_cardinality = '1'
