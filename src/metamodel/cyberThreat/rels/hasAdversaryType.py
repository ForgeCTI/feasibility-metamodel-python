from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.Adversary import Adversary
from metamodel.cyberThreat.entities.AdversaryType import AdversaryType


class hasAdversaryType(BaseRelationship):
    """Adversary --hasAdversaryType--> AdversaryType."""

    label = 'hasAdversaryType'
    source_type = Adversary
    target_type = AdversaryType
    source_cardinality = '0..*'
    target_cardinality = '1..*'
