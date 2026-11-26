from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackToolInstance import AttackToolInstance
from metamodel.cyberThreat.entities.Indicator import Indicator


class associatedToTool(BaseRelationship):
    """Indicator --associatedTo--> AttackToolInstance."""

    label = 'associatedTo'
    source_type = Indicator
    target_type = AttackToolInstance
    source_cardinality = '0..*'
    target_cardinality = '0..1'
