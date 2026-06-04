from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.Resource import Resource


class hostsResource(BaseRelationship):
    """Connects Node to Resource."""

    source_type = Node
    target_type = Resource
    source_cardinality = '1'
    target_cardinality = '1..*'
