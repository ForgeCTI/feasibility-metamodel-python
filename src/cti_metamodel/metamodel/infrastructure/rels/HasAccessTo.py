from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.User import User
from ..entities.Node import Node

class HasAccessToRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasAccessTo",
            src_type=User,
            dst_type=Node,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="User has access to one or more Nodes.",
        )