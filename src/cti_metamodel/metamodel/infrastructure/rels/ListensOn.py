from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.Process import Process
from src.metamodel.infrastructure.entities.Port import Port

class ListensOnRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="listensOn",
            src_type=Process,
            dst_type=Port,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="A Process can listen on zero or more Ports for incoming network communication within the infrastructure environment.",
        )