from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.ApplicationInstance import ApplicationInstance
from ..entities.ApplicationType import ApplicationType

class HasApplicationTypeRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasApplicationType",
            src_type=ApplicationInstance,
            dst_type=ApplicationType,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="An ApplicationInstance has one ApplicationType defining its category or classification within the infrastructure environment.",
        )