from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector


class operatesIn(BaseRelationship):
    """Organization --operatesIn--> Sector."""

    label = 'operatesIn'
    source_type = Organization
    target_type = Sector
    source_cardinality = '0..*'
    target_cardinality = '1..*'
