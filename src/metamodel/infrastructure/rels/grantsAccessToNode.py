from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Account import Account
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.PrivilegeLevel import PrivilegeLevel


class grantsAccessToNode(BaseRelationship):
    """Account --grantsAccessTo--> Node.

    The association class PrivilegeLevel is the attribute ``privilege_level``."""

    label = 'grantsAccessTo'
    source_type = Account
    target_type = Node
    source_cardinality = '0..*'
    target_cardinality = '0..*'
    _domain_attributes = ('privilege_level',)
    _entity_attributes = {'privilege_level': PrivilegeLevel}
