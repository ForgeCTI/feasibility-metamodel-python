from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.HomeCountry import HomeCountry


class basedIn(BaseRelationship):
    """Connects Organization to HomeCountry."""

    source_type = Organization
    target_type = HomeCountry
    source_cardinality = '1'
    target_cardinality = None
