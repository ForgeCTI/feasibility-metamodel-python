from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.BusinessRequirement import BusinessRequirement
from metamodel.organization.entities.Organization import Organization


class hasBusinessRequirement(BaseRelationship):
    """Organization --hasBusinessRequirement--> BusinessRequirement."""

    label = 'hasBusinessRequirement'
    source_type = Organization
    target_type = BusinessRequirement
    source_cardinality = '1'
    target_cardinality = '1..*'
