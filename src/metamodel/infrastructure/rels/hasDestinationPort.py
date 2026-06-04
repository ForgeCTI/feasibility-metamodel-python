from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Connection import Connection
from metamodel.infrastructure.entities.Port import Port


class hasDestinationPort(BaseRelationship):
    """Connects Connection to Port."""

    source_type = Connection
    target_type = Port
    source_cardinality = '1..*'
    target_cardinality = '1'
