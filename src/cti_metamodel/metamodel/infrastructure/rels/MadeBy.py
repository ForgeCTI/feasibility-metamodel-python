from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.Infrastructure import Infrastructure
from src.metamodel.infrastructure.entities.Node import Node

class MadeByRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="madeBy",
            src_type=Infrastructure,
            dst_type=Node,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Infrastructure is made by one or more Nodes.",
        )