from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolConfiguration import AttackToolConfiguration
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance


class hasConfig(BaseRelationship):
    """AttackToolInstance --hasConfig--> AttackToolConfiguration."""

    label = 'hasConfig'
    source_type = AttackToolInstance
    target_type = AttackToolConfiguration
    source_cardinality = '0..*'
    target_cardinality = '0..*'
