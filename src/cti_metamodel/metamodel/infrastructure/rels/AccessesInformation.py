from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.User import User
from ..entities.Information import Information

class AccessesInformationRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="accessesInformation",
            src_type=User,
            dst_type=Information,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="A User can access zero or more Information entities within the infrastructure environment.",
        )
