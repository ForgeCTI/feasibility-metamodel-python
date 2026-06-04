from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.OSInstance import OSInstance
from metamodel.infrastructure.entities.OS import OS


class osInstanceOf(BaseRelationship):
    """Connects OSInstance to OS."""

    source_type = OSInstance
    target_type = OS
    source_cardinality = '0..*'
    target_cardinality = '1'
