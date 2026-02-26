from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.SoftwareVulnerability import SoftwareVulnerability
from ..entities.Process import Process

class AffectsProcessRelationship(BaseRelationship):
    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="affectsProcess",
            src_type=SoftwareVulnerability,
            dst_type=Process,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="A SoftwareVulnerability can affect zero or more Processes within the infrastructure environment.",
        )
