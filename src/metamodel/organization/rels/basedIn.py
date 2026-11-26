from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.HomeCountry import HomeCountry
from metamodel.organization.entities.Organization import Organization


class basedIn(BaseRelationship):
    """Organization --basedIn--> HomeCountry."""

    label = 'basedIn'
    source_type = Organization
    target_type = HomeCountry
    source_cardinality = '0..*'
    target_cardinality = '1..*'
