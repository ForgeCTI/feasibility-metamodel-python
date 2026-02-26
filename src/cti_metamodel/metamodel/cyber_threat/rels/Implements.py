from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackStepItem import AttackStepItem
from ..entities.TTP import TTP

class ImplementsRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackStepItem implements a TTP.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="implements",
            src_type=AttackStepItem,
            dst_type=TTP,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="An AttackStepItem implements a TTP.",
        )