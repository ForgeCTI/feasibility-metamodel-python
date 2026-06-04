from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.Node import Node


class hasAccessTo(BaseRelationship):
    """Connects User to Node."""

    source_type = User
    target_type = Node
    source_cardinality = None
    target_cardinality = None
