from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Code import Code
from metamodel.cyberThreat.entities.ConfigVulnerability import ConfigVulnerability


class affectsCode(BaseRelationship):
    """ConfigVulnerability --affects--> Code."""

    label = 'affects'
    source_type = ConfigVulnerability
    target_type = Code
    source_cardinality = '0..*'
    target_cardinality = '0..*'
