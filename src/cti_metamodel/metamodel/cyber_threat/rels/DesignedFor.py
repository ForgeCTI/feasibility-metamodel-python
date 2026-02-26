from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ...infrastructure.entities.OS import OS
from ..entities.AttackToolInstance import AttackToolInstance

class DesignedForRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackToolInstance is designed for a specific OS.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="designedFor",
            src_type=AttackToolInstance,
            dst_type=OS,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="An AttackToolInstance is designed for a specific OS.",
        )