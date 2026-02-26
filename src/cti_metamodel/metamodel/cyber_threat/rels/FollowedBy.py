from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackStepItem import AttackStepItem

class FollowedByRelationship(BaseRelationship):
    """
    Relationship indicating that one AttackStepItem is followed by another AttackStepItem.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="followedBy",
            src_type=AttackStepItem,
            dst_type=AttackStepItem,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Indicates that one AttackStepItem is followed by another AttackStepItem.",
        )
