from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.cyberThreat.entities.AttackTool import AttackTool
from metamodel.cyberThreat.entities.Expertise import Expertise


class requiresExpertise(BaseRelationship):
    """Connects AttackTool to Expertise."""

    source_type = AttackTool
    target_type = Expertise
    source_cardinality = None
    target_cardinality = None
