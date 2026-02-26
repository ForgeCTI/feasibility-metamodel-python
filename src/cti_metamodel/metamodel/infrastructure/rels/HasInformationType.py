from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Information import Information
from ..entities.InformationType import InformationType

class HasInformationTypeRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasInformationType",
            src_type=Information,
            dst_type=InformationType,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="Information has exactly one InformationType.",
        )