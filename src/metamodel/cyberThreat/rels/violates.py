from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement


class violates(BaseRelationship):
    """Connects TTP to SecurityRequirement."""

    source_type = TTP
    target_type = SecurityRequirement
    source_cardinality = '1..*'
    target_cardinality = '1..*'
