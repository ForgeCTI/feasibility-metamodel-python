from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.NodeType import NodeType


class hasNodeType(BaseRelationship):
    """Node --hasNodeType--> NodeType."""

    label = 'hasNodeType'
    source_type = Node
    target_type = NodeType
    source_cardinality = '0..*'
    target_cardinality = '1'
