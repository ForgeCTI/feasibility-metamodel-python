from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Campaign import Campaign
from ...organization.entities.Sector import Sector

class TargetsSectorRelationship(BaseRelationship):
    """
    Relationship indicating that a Campaign targets a specific Sector.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="targetsSector",
            src_type=Campaign,
            dst_type=Sector,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Indicates that a Campaign targets a specific Sector.",
        )