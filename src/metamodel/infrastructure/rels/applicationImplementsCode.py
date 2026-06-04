from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.Code import Code


class applicationImplementsCode(BaseRelationship):
    """Connects ApplicationInstance to Code."""

    source_type = ApplicationInstance
    target_type = Code
    source_cardinality = None
    target_cardinality = None
