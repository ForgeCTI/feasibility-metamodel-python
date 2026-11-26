from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Application import Application
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance


class applicationInstanceOf(BaseRelationship):
    """ApplicationInstance --instanceOf--> Application."""

    label = 'instanceOf'
    source_type = ApplicationInstance
    target_type = Application
    source_cardinality = '0..*'
    target_cardinality = '1'
