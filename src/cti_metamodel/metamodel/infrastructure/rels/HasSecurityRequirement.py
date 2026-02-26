from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.Asset import Asset
from src.metamodel.infrastructure.entities.AssetSecurityRequirement import AssetSecurityRequirement

class HasSecurityRequirement(BaseRelationship):
    """
    Relationship indicating that an Asset has a specific Security Requirement.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasSecurityRequirement",
            src_type=Asset,
            dst_type=AssetSecurityRequirement,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Asset has one or more Security Requirements.",
        )