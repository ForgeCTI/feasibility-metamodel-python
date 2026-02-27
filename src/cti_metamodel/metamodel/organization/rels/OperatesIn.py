from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship
from ..entities.Organization import Organization
from ..entities.Sector import Sector

class OperatesInRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="operatesIn",
            src_type=Organization,
            dst_type=Sector,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="An Organization may operate in one or more Sector.",
        )