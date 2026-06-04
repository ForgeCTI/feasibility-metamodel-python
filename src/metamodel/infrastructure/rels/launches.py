from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.Code import Code


class launches(BaseRelationship):
    """Connects User to Code."""

    source_type = User
    target_type = Code
    source_cardinality = '1'
    target_cardinality = '0..*'
