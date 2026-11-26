from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.UserType import UserType


class hasUserType(BaseRelationship):
    """User --hasUserType--> UserType."""

    label = 'hasUserType'
    source_type = User
    target_type = UserType
    source_cardinality = '0..*'
    target_cardinality = '1'
