from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.OS import OS
from ..entities.Node import Node

class RunsOSRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="runsOS",
            src_type=Node,
            dst_type=OS,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="A Node runs exactly one Operating System (OS) within the infrastructure environment.",
        )
