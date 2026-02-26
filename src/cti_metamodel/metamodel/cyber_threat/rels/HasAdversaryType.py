from __future__ import annotations

from ....core.Cardinality import Cardinality
from ....core.BaseRelationship import BaseRelationship

from ..entities.Adversary import Adversary
from ..entities.AdversaryType import AdversaryType

class HasAdversaryTypeRelationship(BaseRelationship):
    """
    Relationship indicating that an Adversary has a specific AdversaryType.
    """

    def __init__(self, src: str, dst: str) -> None:
        super().__init__(
            name="hasAdversaryType",
            src_type=Adversary,
            dst_type=AdversaryType,
            src=src,
            dst=dst,
            cardinality=Cardinality(1, 1),
            description="An Adversary has a specific AdversaryType.",
        )