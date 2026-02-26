from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.AttackToolInstance import AttackToolInstance
from ..entities.AttackToolConfiguration import AttackToolConfiguration

class HasConfigRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackToolInstance has an AttackToolConfiguration.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasConfig",
            src_type=AttackToolInstance,
            dst_type=AttackToolConfiguration,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, 1),
            description="An AttackToolInstance has an AttackToolConfiguration.",
        )
