from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackToolInstance import AttackToolInstance
from ..entities.Indicator import Indicator

class ProducesRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackToolInstance produces an Indicator.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="produces",
            src_type=AttackToolInstance,
            dst_type=Indicator,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="An AttackToolInstance produces an Indicator.",
        )