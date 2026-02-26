from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackStepItem import AttackStepItem
from ..entities.AttackToolInstance import AttackToolInstance

class EmploysRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackToolInstance employs an AttackStepItem.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="employs",
            src_type=AttackStepItem,
            dst_type=AttackToolInstance,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="An AttackStepItem employs an AttackToolInstance.",
        )
