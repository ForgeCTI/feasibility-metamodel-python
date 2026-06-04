from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.AttackTool import AttackTool


class toolInstanceOf(BaseRelationship):
    """Connects AttackToolInstance to AttackTool."""

    source_type = AttackToolInstance
    target_type = AttackTool
    source_cardinality = '1..*'
    target_cardinality = '1'
