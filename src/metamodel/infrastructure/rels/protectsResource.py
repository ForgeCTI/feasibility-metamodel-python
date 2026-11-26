from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.infrastructure.entities.SecurityControl import SecurityControl


class protectsResource(BaseRelationship):
    """SecurityControl --protects--> Resource."""

    label = 'protects'
    source_type = SecurityControl
    target_type = Resource
    source_cardinality = '0..*'
    target_cardinality = '0..*'
