from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.SecurityRequirement import SecurityRequirement
from ..entities.AssetSecurityRequirement import AssetSecurityRequirement

class ImplementationOfRelationship(BaseRelationship):
    """
    Relationship indicating that an AssetSecurityRequirement is an implementation of a SecurityRequirement.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="implementationOf",
            src_type=AssetSecurityRequirement,
            dst_type=SecurityRequirement,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="An AssetSecurityRequirement is an implementation of a SecurityRequirement.",
        )