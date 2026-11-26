from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Account import Account
from metamodel.infrastructure.entities.PrivilegeLevel import PrivilegeLevel
from metamodel.infrastructure.entities.Resource import Resource


class grantsAccessToResource(BaseRelationship):
    """Account --grantsAccessTo--> Resource.

    The association class PrivilegeLevel is the attribute ``privilege_level``."""

    label = 'grantsAccessTo'
    source_type = Account
    target_type = Resource
    source_cardinality = '0..*'
    target_cardinality = '1..*'
    _domain_attributes = ('privilege_level',)
    _entity_attributes = {'privilege_level': PrivilegeLevel}
