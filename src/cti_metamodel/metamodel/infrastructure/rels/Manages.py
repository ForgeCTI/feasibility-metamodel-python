from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship
from src.metamodel.organization.entities.Organization import Organization
from src.metamodel.infrastructure.entities.Infrastructure import Infrastructure

class ManagesRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="manages",
            src_type=Organization,
            dst_type=Infrastructure,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="An Organization manages one or more Infrastructure.",
        )
