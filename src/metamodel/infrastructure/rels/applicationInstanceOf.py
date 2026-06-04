from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.Application import Application


class applicationInstanceOf(BaseRelationship):
    """Connects ApplicationInstance to Application."""

    source_type = ApplicationInstance
    target_type = Application
    source_cardinality = '0..*'
    target_cardinality = '1'
