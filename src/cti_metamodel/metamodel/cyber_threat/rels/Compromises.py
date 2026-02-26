from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackStepItem import AttackStepItem
from ...infrastructure.entities.AssetSecurityRequirement import AssetSecurityRequirement

class CompromisesRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackStepItem compromises an AssetSecurityRequirement.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="compromises",
            src_type=AttackStepItem,
            dst_type=AssetSecurityRequirement,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Indicates that an AttackStepItem compromises an AssetSecurityRequirement.",
        )
