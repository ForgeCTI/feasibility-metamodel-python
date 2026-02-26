from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.ThreatEvent import ThreatEvent
from ..entities.AttackStepItem import AttackStepItem

class StartsWithRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackStepItem starts with a ThreatEvent.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="startsWith",
            src_type=ThreatEvent,
            dst_type=AttackStepItem,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="Indicates that a ThreatEvent starts with an AttackStepItem.",
        )
