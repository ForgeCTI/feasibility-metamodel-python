from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.ConfigVulnerability import ConfigVulnerability
from metamodel.infrastructure.entities.Code import Code


class affectsCode(BaseRelationship):
    """Connects ConfigVulnerability to Code."""

    source_type = ConfigVulnerability
    target_type = Code
    source_cardinality = '0..*'
    target_cardinality = '1..*'
