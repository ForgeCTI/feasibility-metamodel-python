from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Application import Application
from metamodel.cyberThreat.entities.SoftwareVulnerability import SoftwareVulnerability


class affectsApplication(BaseRelationship):
    """SoftwareVulnerability --affects--> Application."""

    label = 'affects'
    source_type = SoftwareVulnerability
    target_type = Application
    source_cardinality = '0..*'
    target_cardinality = '1..*'
