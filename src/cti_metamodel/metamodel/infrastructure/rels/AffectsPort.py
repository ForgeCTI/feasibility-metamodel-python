from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.ConfigVulnerability import ConfigVulnerability
from ..entities.Port import Port

class AffectsPortRelationship(BaseRelationship):
    """
    Represents a relationship where a configuration vulnerability affects a specific port.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="affectsPort",
            src_type=ConfigVulnerability,
            dst_type=Port,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="Configuration Vulnerability affects a Port.",
        )
