from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.organization.entities.HomeCountry import HomeCountry
from metamodel.organization.entities.InternationalBody import InternationalBody


class countryPartOf(BaseRelationship):
    """Connects HomeCountry to InternationalBody."""

    source_type = HomeCountry
    target_type = InternationalBody
    source_cardinality = '1..*'
    target_cardinality = '1..*'
