from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.Organization import Organization
from metamodel.infrastructure.entities.Infrastructure import Infrastructure


class manages(BaseRelationship):
    """Connects Organization to Infrastructure."""

    source_type = Organization
    target_type = Infrastructure
    source_cardinality = '1'
    target_cardinality = '1..*'
