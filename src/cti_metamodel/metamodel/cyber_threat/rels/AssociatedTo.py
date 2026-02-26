from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Indicator import Indicator
from ..entities.AttackToolInstance import AttackToolInstance

class AssociatedToRelationship(BaseRelationship):
    """
    Relationship indicating that an AttackToolInstance is associated to an Indicator.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="associatedTo",
            src_type=Indicator,
            dst_type=AttackToolInstance,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="An AttackToolInstance is associated to an Indicator.",
        )
