from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Process import Process
from ..entities.Information import Information

class AccessesRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="accesses",
            src_type=Process,
            dst_type=Information,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="A Process can access zero or more Information entities within the infrastructure environment.",
        )