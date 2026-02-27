from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship
from ..entities.BusinessRequirement import BusinessRequirement
from ..entities.Organization import Organization

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