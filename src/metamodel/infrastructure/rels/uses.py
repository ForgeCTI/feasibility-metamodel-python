from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.Port import Port


class uses(BaseRelationship):
    """ApplicationInstance --uses--> Port.

    An application instance listens on a port."""

    label = 'uses'
    source_type = ApplicationInstance
    target_type = Port
    source_cardinality = '0..1'
    target_cardinality = '0..*'
