from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.User import User


class usedBy(BaseRelationship):
    """Connects Infrastructure to User."""

    source_type = Infrastructure
    target_type = User
    source_cardinality = '1'
    target_cardinality = '1..*'
