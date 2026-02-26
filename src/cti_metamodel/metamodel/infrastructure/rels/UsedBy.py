from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.Infrastructure import Infrastructure
from src.metamodel.infrastructure.entities.User import User

class UsedByRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="usedBy",
            src_type=Infrastructure,
            dst_type=User,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Infrastructure is used by one or more Users.",
        )
