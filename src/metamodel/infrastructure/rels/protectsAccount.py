from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Account import Account
from metamodel.infrastructure.entities.SecurityControl import SecurityControl


class protectsAccount(BaseRelationship):
    """SecurityControl --protects--> Account."""

    label = 'protects'
    source_type = SecurityControl
    target_type = Account
    source_cardinality = '0..*'
    target_cardinality = '0..*'
