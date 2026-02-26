from __future__ import annotations

from src.core.Cardinality import Cardinality
from src.core.BaseRelationship import BaseRelationship
from src.metamodel.organization.entities import HomeCountry, Organization

class BasedInRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="basedIn",
            src_type=Organization,
            dst_type=HomeCountry,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Organization may be based in one or more HomeCountry jurisdictions.",
        )
