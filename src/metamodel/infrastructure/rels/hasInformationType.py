from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Information import Information
from metamodel.infrastructure.entities.InformationType import InformationType


class hasInformationType(BaseRelationship):
    """Connects Information to InformationType."""

    source_type = Information
    target_type = InformationType
    source_cardinality = '1..*'
    target_cardinality = '1'
