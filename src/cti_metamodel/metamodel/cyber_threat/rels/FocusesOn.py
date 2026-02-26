from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Campaign import Campaign
from ...organization.entities.HomeCountry import HomeCountry

class FocusesOnRelationship(BaseRelationship):
    """
    Relationship indicating that a Campaign focuses on a specific HomeCountry.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="focusesOn",
            src_type=Campaign,
            dst_type=HomeCountry,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Indicates that a Campaign focuses on specific HomeCountries.",
        )