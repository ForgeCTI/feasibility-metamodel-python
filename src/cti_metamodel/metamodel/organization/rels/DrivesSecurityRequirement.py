from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship
from ..entities.BusinessRequirement import BusinessRequirement
from ...infrastructure.entities.AssetSecurityRequirement import AssetSecurityRequirement

class DrivesSecurityRequirementRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="drivesSecurityRequirement",
            src_type=BusinessRequirement,
            dst_type=AssetSecurityRequirement,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="A BusinessRequirement drives one or more AssetSecurityRequirement.",
        )
