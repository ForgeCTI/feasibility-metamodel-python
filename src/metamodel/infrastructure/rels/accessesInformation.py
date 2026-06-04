from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Code import Code
from metamodel.infrastructure.entities.Information import Information


class accessesInformation(BaseRelationship):
    """Connects Code to Information."""

    source_type = Code
    target_type = Information
    source_cardinality = '0..*'
    target_cardinality = '0..*'
