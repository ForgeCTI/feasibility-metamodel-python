from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.SecurityControl import SecurityControl
from metamodel.infrastructure.entities.User import User


class protectsUser(BaseRelationship):
    """SecurityControl --protects--> User."""

    label = 'protects'
    source_type = SecurityControl
    target_type = User
    source_cardinality = '0..*'
    target_cardinality = '0..*'
