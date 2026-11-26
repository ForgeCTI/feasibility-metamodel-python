from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.SecurityControl import SecurityControl


class protectsNode(BaseRelationship):
    """SecurityControl --protects--> Node."""

    label = 'protects'
    source_type = SecurityControl
    target_type = Node
    source_cardinality = '0..*'
    target_cardinality = '0..*'
