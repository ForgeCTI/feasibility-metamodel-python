from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.SoftwareVulnerability import SoftwareVulnerability
from metamodel.infrastructure.entities.Application import Application


class affectsApplication(BaseRelationship):
    """Connects SoftwareVulnerability to Application."""

    source_type = SoftwareVulnerability
    target_type = Application
    source_cardinality = '0..*'
    target_cardinality = '1'
