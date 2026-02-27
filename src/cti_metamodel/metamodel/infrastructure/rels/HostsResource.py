from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Node import Node
from ..entities.Resource import Resource

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
