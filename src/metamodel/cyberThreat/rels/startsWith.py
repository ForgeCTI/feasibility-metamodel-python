from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep


class startsWith(BaseRelationship):
    """Threat --startsWith--> ThreatStep.

    Paper figure: 1 at the Threat end, which would make every step a first step; relaxed to 0..* (a step may start several threats)."""

    label = 'startsWith'
    source_type = Threat
    target_type = ThreatStep
    source_cardinality = '0..*'
    target_cardinality = '1..*'
