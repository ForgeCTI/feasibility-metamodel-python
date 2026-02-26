from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ...cyber_threat.entities.TTP import TTP
from ...infrastructure.entities.AssetSecurityRequirement import AssetSecurityRequirement

class ImpactsRelationship(BaseRelationship):
    """
    Relationship indicating that a TTP impacts an AssetSecurityRequirement.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="impacts",
            src_type=TTP,
            dst_type=AssetSecurityRequirement,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="A TTP impacts an AssetSecurityRequirement.",
        )
