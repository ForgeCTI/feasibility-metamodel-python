from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance


class runsApp(BaseRelationship):
    """Connects Node to ApplicationInstance."""

    source_type = Node
    target_type = ApplicationInstance
    source_cardinality = '1'
    target_cardinality = '0..*'
