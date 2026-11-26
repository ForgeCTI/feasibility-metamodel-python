from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.SecurityControl import SecurityControl
from metamodel.cyberThreat.entities.Vulnerability import Vulnerability


class mitigates(BaseRelationship):
    """SecurityControl --mitigates--> Vulnerability."""

    label = 'mitigates'
    source_type = SecurityControl
    target_type = Vulnerability
    source_cardinality = '0..*'
    target_cardinality = '0..*'
