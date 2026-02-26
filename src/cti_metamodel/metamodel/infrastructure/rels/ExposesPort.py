from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Node import Node
from ..entities.Port import Port

class ExposesPortRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="exposesPort",
            src_type=Node,
            dst_type=Port,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="A Node can expose zero or more Ports for communication within the infrastructure environment.",
        )