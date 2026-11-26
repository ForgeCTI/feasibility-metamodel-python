from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Code import Code
from metamodel.infrastructure.entities.Port import Port


class listensOn(BaseRelationship):
    """Connects Code to Port."""

    source_type = Code
    target_type = Port
    source_cardinality = '1'
    target_cardinality = '0..*'
