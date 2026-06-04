from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.Indicator import Indicator


class producesIndicator(BaseRelationship):
    """Connects AttackToolInstance to Indicator."""

    source_type = AttackToolInstance
    target_type = Indicator
    source_cardinality = '1'
    target_cardinality = '1..*'
