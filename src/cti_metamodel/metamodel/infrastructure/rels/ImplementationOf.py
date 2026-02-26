from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship

from src.metamodel.infrastructure.entities.SecurityRequirement import SecurityRequirement
from src.metamodel.infrastructure.entities.AssetSecurityRequirement import AssetSecurityRequirement

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