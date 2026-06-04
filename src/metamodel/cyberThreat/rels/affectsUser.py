from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.HumanVulnerability import HumanVulnerability
from metamodel.infrastructure.entities.User import User


class affectsUser(BaseRelationship):
    """Connects HumanVulnerability to User."""

    source_type = HumanVulnerability
    target_type = User
    source_cardinality = '0..*'
    target_cardinality = '0..*'
