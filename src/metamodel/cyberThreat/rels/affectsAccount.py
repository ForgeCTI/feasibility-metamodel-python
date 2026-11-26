from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Account import Account
from metamodel.cyberThreat.entities.ConfigVulnerability import ConfigVulnerability


class affectsAccount(BaseRelationship):
    """ConfigVulnerability --affects--> Account."""

    label = 'affects'
    source_type = ConfigVulnerability
    target_type = Account
    source_cardinality = '0..*'
    target_cardinality = '0..*'
