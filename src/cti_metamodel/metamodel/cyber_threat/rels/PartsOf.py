from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.ThreatEvent import ThreatEvent
from ..entities.Campaign import Campaign

class PartsOfRelationship(BaseRelationship):
    """
    Relationship indicating that a Campaign is part of a ThreatEvent.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="partsOf",
            src_type=Campaign,
            dst_type=ThreatEvent,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="Indicates that a Campaign is part of a ThreatEvent.",
        )