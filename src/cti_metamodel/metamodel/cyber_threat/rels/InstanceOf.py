from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackToolInstance import AttackToolInstance
from ..entities.AttackTool import AttackTool

class InstanceOfRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackToolInstance is an instance of an AttackTool.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="instanceOf",
            src_type=AttackToolInstance,
            dst_type=AttackTool,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="An AttackToolInstance is an instance of an AttackTool.",
        )