from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship
from ...organization.entities.Organization import Organization
from ..entities.Infrastructure import Infrastructure

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
