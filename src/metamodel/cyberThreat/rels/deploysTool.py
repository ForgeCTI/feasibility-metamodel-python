from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance


class deploysTool(BaseRelationship):
    """AttackToolInstance --deploys--> AttackToolInstance."""

    label = 'deploys'
    source_type = AttackToolInstance
    target_type = AttackToolInstance
    source_cardinality = '0..*'
    target_cardinality = '0..*'
