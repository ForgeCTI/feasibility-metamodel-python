from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship
from src.metamodel.organization.entities import HomeCountry, InternationalBody

class PartsOfRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="partsOf",
            src_type=InternationalBody,
            dst_type=HomeCountry,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="An InternationalBody may include one or more HomeCountry.",
        )
