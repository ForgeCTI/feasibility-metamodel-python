from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Connection import Connection
from ..entities.Port import Port

class HasDestinationPortRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasDestinationPort",
            src_type=Connection,
            dst_type=Port,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="A Connection has exactly one destination Port for communication within the infrastructure environment.",
        )
