from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Adversary import Adversary
from metamodel.cyberThreat.entities.AdversaryType import AdversaryType


class hasAdversaryType(BaseRelationship):
    """Connects Adversary to AdversaryType."""

    source_type = Adversary
    target_type = AdversaryType
    source_cardinality = '1..*'
    target_cardinality = '1'
