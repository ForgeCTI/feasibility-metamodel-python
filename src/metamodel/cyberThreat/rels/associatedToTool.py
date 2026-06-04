from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Indicator import Indicator
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance


class associatedToTool(BaseRelationship):
    """Connects Indicator to AttackToolInstance."""

    source_type = Indicator
    target_type = AttackToolInstance
    source_cardinality = '1..*'
    target_cardinality = '1'
