from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance


class toolInstanceOf(BaseRelationship):
    """AttackToolInstance --instanceOf--> AttackTool."""

    label = 'instanceOf'
    source_type = AttackToolInstance
    target_type = AttackTool
    source_cardinality = '0..*'
    target_cardinality = '1'
