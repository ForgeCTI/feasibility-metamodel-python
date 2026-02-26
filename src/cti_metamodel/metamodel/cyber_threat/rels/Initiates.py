from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.ThreatSource import ThreatSource
from ..entities.ThreatEvent import ThreatEvent

class InitiatesRelationship(BaseRelationship):
    """
    Relationship indicating that a ThreatSource initiates a ThreatEvent.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="initiates",
            src_type=ThreatSource,
            dst_type=ThreatEvent,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Indicates that a ThreatSource initiates a ThreatEvent.",
        )