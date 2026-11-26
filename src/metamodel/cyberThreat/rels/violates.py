from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement
from metamodel.cyberThreat.entities.TTP import TTP


class violates(BaseRelationship):
    """TTP --violates--> SecurityRequirement."""

    label = 'violates'
    source_type = TTP
    target_type = SecurityRequirement
    source_cardinality = '0..*'
    target_cardinality = '0..*'
