from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.OSInstance import OSInstance


class runsOS(BaseRelationship):
    """Node --runsOS--> OSInstance."""

    label = 'runsOS'
    source_type = Node
    target_type = OSInstance
    source_cardinality = '1'
    target_cardinality = '0..1'
