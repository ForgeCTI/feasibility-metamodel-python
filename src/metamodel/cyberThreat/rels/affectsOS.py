from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.SoftwareVulnerability import SoftwareVulnerability
from metamodel.infrastructure.entities.OS import OS


class affectsOS(BaseRelationship):
    """Connects SoftwareVulnerability to OS."""

    source_type = SoftwareVulnerability
    target_type = OS
    source_cardinality = '1..*'
    target_cardinality = '1'
