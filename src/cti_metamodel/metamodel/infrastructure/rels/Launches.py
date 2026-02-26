from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.User import User
from src.metamodel.infrastructure.entities.Process import Process

class LaunchesRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="launches",
            src_type=User,
            dst_type=Process,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="A User can launch zero or more Processes within the infrastructure environment.",
        )