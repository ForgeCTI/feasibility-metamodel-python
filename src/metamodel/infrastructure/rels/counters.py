from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.SecurityControlType import SecurityControlType
from metamodel.cyberThreat.entities.TTP import TTP


class counters(BaseRelationship):
    """SecurityControlType --counters--> TTP.

    Asserted only when the control type prevents the technique by design (curated)."""

    label = 'counters'
    source_type = SecurityControlType
    target_type = TTP
    source_cardinality = '0..*'
    target_cardinality = '0..*'
