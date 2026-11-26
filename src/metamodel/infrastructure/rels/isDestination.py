from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Connection import Connection
from metamodel.infrastructure.entities.Node import Node


class isDestination(BaseRelationship):
    """Node --isDestination--> Connection."""

    label = 'isDestination'
    source_type = Node
    target_type = Connection
    source_cardinality = '0..1'
    target_cardinality = '0..*'
