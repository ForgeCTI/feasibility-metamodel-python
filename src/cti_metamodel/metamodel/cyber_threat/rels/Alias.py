from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.ThreatSource import ThreatSource

class AliasRelationship(BaseRelationship):
    """
    Relationship indicating that one ThreatSource is an alias of another ThreatSource.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="alias",
            src_type=ThreatSource,
            dst_type=ThreatSource,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, None),
            description="Indicates that one ThreatSource is an alias of another ThreatSource.",
        )