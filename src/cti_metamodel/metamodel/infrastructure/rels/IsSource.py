from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.Node import Node
from src.metamodel.infrastructure.entities.Connection import Connection

class IsSourceRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="isSource",
            src_type=Node,
            dst_type=Connection,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="A Node can be the source of one or more Connections within the infrastructure environment.",
        )