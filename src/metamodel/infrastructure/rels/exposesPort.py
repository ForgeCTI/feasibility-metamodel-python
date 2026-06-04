from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.Port import Port


class exposesPort(BaseRelationship):
    """Connects Node to Port."""

    source_type = Node
    target_type = Port
    source_cardinality = '1'
    target_cardinality = '1..*'
