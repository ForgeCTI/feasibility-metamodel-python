from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackToolInstance import AttackToolInstance

class DeploysRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackToolInstance deploys another AttackToolInstance.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="deploys",
            src_type=AttackToolInstance,
            dst_type=AttackToolInstance,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="An AttackToolInstance deploys another AttackToolInstance.",
        )