from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.Node import Node


class runs(BaseRelationship):
    """Connects Node to Node."""

    source_type = Node
    target_type = Node
    source_cardinality = '1'
    target_cardinality = '1..*'
