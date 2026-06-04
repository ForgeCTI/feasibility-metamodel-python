from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.Connection import Connection


class isDestination(BaseRelationship):
    """Connects Node to Connection."""

    source_type = Node
    target_type = Connection
    source_cardinality = '1'
    target_cardinality = '0..*'
