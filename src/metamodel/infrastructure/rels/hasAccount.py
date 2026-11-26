from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Account import Account
from metamodel.infrastructure.entities.User import User


class hasAccount(BaseRelationship):
    """User --hasAccount--> Account."""

    label = 'hasAccount'
    source_type = User
    target_type = Account
    source_cardinality = '1'
    target_cardinality = '0..*'
