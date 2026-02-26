from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.Node import Node
from src.metamodel.infrastructure.entities.Resource import Resource

class HostsResourceRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hostsResource",
            src_type=Node,
            dst_type=Resource,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Node hosts one or more Resources.",
        )
