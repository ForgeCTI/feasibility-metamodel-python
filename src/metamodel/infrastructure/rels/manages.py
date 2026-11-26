from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.organization.entities.Organization import Organization


class manages(BaseRelationship):
    """Organization --manages--> Infrastructure."""

    label = 'manages'
    source_type = Organization
    target_type = Infrastructure
    source_cardinality = '1'
    target_cardinality = '1..*'
