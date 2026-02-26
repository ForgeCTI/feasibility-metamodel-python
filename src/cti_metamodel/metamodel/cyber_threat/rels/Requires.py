from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackTool import AttackTool
from ..entities.AttackToolConfiguration import AttackToolConfiguration

class RequiresRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackTool requires an AttackToolConfiguration.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="requires",
            src_type=AttackTool,
            dst_type=AttackToolConfiguration,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="An AttackTool requires an AttackToolConfiguration.",
        )
