from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Node import Node
from ..entities.Connection import Connection

class IsDestinationRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="isDestination",
            src_type=Node,
            dst_type=Connection,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="A Node can be the destination of one or more Connections within the infrastructure environment.",
        )