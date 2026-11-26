from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep


class employsTool(BaseRelationship):
    """ThreatStep --employs--> AttackToolInstance."""

    label = 'employs'
    source_type = ThreatStep
    target_type = AttackToolInstance
    source_cardinality = '0..*'
    target_cardinality = '0..*'
