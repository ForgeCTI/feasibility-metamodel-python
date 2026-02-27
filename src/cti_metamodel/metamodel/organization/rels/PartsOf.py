from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship
from ..entities.HomeCountry import HomeCountry
from ..entities.InternationalBody import InternationalBody

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
