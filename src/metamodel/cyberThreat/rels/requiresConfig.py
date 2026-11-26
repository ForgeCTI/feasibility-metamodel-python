from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.AttackToolConfiguration import AttackToolConfiguration


class requiresConfig(BaseRelationship):
    """AttackTool --requires--> AttackToolConfiguration."""

    label = 'requires'
    source_type = AttackTool
    target_type = AttackToolConfiguration
    source_cardinality = '0..*'
    target_cardinality = '0..*'
