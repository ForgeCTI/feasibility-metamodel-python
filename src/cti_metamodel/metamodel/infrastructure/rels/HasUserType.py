from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.User import User
from src.metamodel.infrastructure.entities.UserType import UserType

class HasUserTypeRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasUserType",
            src_type=User,
            dst_type=UserType,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="User has exactly one UserType.",
        )
