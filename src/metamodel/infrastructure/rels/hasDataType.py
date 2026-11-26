from __future__ import annotations

from metamodel.core.BaseRelationship import BaseRelationship
from metamodel.infrastructure.entities.Data import Data
from metamodel.infrastructure.entities.DataType import DataType


class hasDataType(BaseRelationship):
    """Data --hasDataType--> DataType."""

    label = 'hasDataType'
    source_type = Data
    target_type = DataType
    source_cardinality = '0..*'
    target_cardinality = '1'
