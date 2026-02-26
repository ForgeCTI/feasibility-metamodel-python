from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship
from src.metamodel.organization.entities import BusinessRequirement
from src.metamodel.infrastructure.entities.AssetSecurityRequirement import AssetSecurityRequirement

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
