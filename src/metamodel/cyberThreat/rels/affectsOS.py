from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.OS import OS
from metamodel.cyberThreat.entities.SoftwareVulnerability import SoftwareVulnerability


class affectsOS(BaseRelationship):
    """SoftwareVulnerability --affects--> OS."""

    label = 'affects'
    source_type = SoftwareVulnerability
    target_type = OS
    source_cardinality = '0..*'
    target_cardinality = '1..*'
