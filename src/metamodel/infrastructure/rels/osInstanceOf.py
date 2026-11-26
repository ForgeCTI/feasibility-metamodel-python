from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.OS import OS
from metamodel.infrastructure.entities.OSInstance import OSInstance


class osInstanceOf(BaseRelationship):
    """OSInstance --instanceOf--> OS."""

    label = 'instanceOf'
    source_type = OSInstance
    target_type = OS
    source_cardinality = '0..*'
    target_cardinality = '1'
