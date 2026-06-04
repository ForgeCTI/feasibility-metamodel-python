from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance


class employsTool(BaseRelationship):
    """Connects ThreatStep to AttackToolInstance."""

    source_type = ThreatStep
    target_type = AttackToolInstance
    source_cardinality = '1..*'
    target_cardinality = '0..*'
