from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Infrastructure import Infrastructure
from ..entities.User import User

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
