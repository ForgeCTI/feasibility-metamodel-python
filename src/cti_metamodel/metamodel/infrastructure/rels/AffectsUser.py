from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.HumanVulnerability import HumanVulnerability
from ..entities.User import User

class AffectsUserRelationship(BaseRelationship):
    """
    Represents a relationship where a human vulnerability affects a specific user.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="affectsUser",
            src_type=HumanVulnerability,
            dst_type=User,
            src=src,
            dst=dst,
            cardinality=Cardinality(0, None),
            description="Human Vulnerability affects a User.",
        )
