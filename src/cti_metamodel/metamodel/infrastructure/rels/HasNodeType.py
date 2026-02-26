from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ....metamodel.infrastructure.entities.Node import Node
from ....metamodel.infrastructure.entities.NodeType import NodeType

class HasNodeTypeRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasNodeType",
            src_type=Node,
            dst_type=NodeType,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="Node has exactly one NodeType.",
        )
