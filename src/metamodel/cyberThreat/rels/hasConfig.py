from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.AttackToolConfiguration import AttackToolConfiguration


class hasConfig(BaseRelationship):
    """Connects AttackToolInstance to AttackToolConfiguration."""

    source_type = AttackToolInstance
    target_type = AttackToolConfiguration
    source_cardinality = '1'
    target_cardinality = '0..*'
