from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.PrivilegeLevel import PrivilegeLevel
from metamodel.infrastructure.entities.Resource import Resource


class requiresPrivilegeLevel(BaseRelationship):
    """Resource --requiresPrivilegeLevel--> PrivilegeLevel."""

    label = 'requiresPrivilegeLevel'
    source_type = Resource
    target_type = PrivilegeLevel
    source_cardinality = '0..*'
    target_cardinality = '0..1'
