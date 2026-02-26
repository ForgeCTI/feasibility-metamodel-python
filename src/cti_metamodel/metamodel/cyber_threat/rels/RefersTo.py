from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackStepItem import AttackStepItem
from ..entities.AttackStep import AttackStep

class RefersToRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackStepItem refers to an AttackStep.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="refersTo",
            src_type=AttackStepItem,
            dst_type=AttackStep,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="An AttackStepItem refers to an AttackStep.",
        )