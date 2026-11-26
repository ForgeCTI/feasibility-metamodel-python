from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.organization.entities.Asset import Asset


class resourceImplementsAsset(BaseRelationship):
    """Connects Resource to Asset."""

    source_type = Resource
    target_type = Asset
    source_cardinality = None
    target_cardinality = None
