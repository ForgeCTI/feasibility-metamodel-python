from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.infrastructure.entities.Node import Node


class deployedTo(BaseRelationship):
    """Connects AttackToolInstance to Node."""

    source_type = AttackToolInstance
    target_type = Node
    source_cardinality = '0..*'
    target_cardinality = '0..1'
