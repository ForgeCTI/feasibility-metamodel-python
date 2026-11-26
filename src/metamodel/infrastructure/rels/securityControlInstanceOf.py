from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.SecurityControl import SecurityControl
from metamodel.infrastructure.entities.SecurityControlType import SecurityControlType


class securityControlInstanceOf(BaseRelationship):
    """SecurityControl --instanceOf--> SecurityControlType."""

    label = 'instanceOf'
    source_type = SecurityControl
    target_type = SecurityControlType
    source_cardinality = '0..*'
    target_cardinality = '1'
