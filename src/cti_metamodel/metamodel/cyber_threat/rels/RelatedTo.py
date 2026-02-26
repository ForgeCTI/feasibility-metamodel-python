from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.ThreatSource import ThreatSource
from ..entities.Adversary import Adversary

class RelatedToRelationship(BaseRelationship):
    """
    Relationship indicating that a ThreatSource is related to an Adversary.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="relatedTo",
            src_type=ThreatSource,
            dst_type=Adversary,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Indicates that a ThreatSource is related to an Adversary.",
        )