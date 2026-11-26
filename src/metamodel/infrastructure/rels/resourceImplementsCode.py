from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.infrastructure.entities.Code import Code


class resourceImplementsCode(BaseRelationship):
    """Connects Resource to Code."""

    source_type = Resource
    target_type = Code
    source_cardinality = None
    target_cardinality = None
