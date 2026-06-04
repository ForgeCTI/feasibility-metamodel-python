from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.infrastructure.entities.OSInstance import OSInstance


class designedFor(BaseRelationship):
    """Connects AttackToolInstance to OSInstance."""

    source_type = AttackToolInstance
    target_type = OSInstance
    source_cardinality = '1..*'
    target_cardinality = '1'
