from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance


class deploysTool(BaseRelationship):
    """Connects AttackToolInstance to AttackToolInstance."""

    source_type = AttackToolInstance
    target_type = AttackToolInstance
    source_cardinality = '0..*'
    target_cardinality = None
