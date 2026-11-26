from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node


class madeBy(BaseRelationship):
    """Infrastructure --madeBy--> Node."""

    label = 'madeBy'
    source_type = Infrastructure
    target_type = Node
    source_cardinality = '1'
    target_cardinality = '1..*'
