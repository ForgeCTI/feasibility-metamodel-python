from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.Resource import Resource


class hostsResource(BaseRelationship):
    """Node --hostsResource--> Resource.

    Application and OS instances run by a node (runsApp, runsOS) count as hosted resources."""

    label = 'hostsResource'
    source_type = Node
    target_type = Resource
    source_cardinality = '1..*'
    target_cardinality = '1..*'
    cardinality_counts = ('runsApp', 'runsOS')
