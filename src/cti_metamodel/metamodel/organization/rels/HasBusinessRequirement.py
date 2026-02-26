from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship
from src.metamodel.organization.entities import BusinessRequirement, Organization

class HasBusinessRequirementRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasBusinessRequirement",
            src_type=Organization,
            dst_type=BusinessRequirement,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="An Organization may have zero or more BusinessRequirement.",
        )