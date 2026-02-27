from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Node import Node
from ..entities.Connection import Connection

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