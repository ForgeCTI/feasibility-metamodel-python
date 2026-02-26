from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship
from src.metamodel.organization.entities import Organization, Sector

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