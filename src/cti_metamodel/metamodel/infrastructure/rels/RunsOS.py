from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.OS import OS
from src.metamodel.infrastructure.entities.Node import Node

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
