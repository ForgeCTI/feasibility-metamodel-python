from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.Information import Information


class userAccessesInformation(BaseRelationship):
    """Connects User to Information."""

    source_type = User
    target_type = Information
    source_cardinality = '1..*'
    target_cardinality = '0..*'
