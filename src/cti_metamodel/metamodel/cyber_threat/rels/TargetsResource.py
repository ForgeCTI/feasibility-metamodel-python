from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackStepItem import AttackStepItem
from ...infrastructure.entities.Resource import Resource

class TargetsResourceRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackStepItem targets a Resource.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="targetsResource",
            src_type=AttackStepItem,
            dst_type=Resource,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Indicates that an AttackStepItem targets a Resource.",
        )
