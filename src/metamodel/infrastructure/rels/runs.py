from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node


class runs(BaseRelationship):
    """Node --runs--> Node.

    A node runs another node, e.g. a container or a virtual machine."""

    label = 'runs'
    source_type = Node
    target_type = Node
    source_cardinality = '0..1'
    target_cardinality = '0..*'
