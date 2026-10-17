from __future__ import annotations

from uuid import uuid4

from metamodel.core.BaseEntity import BaseEntity


class BaseRelationship:
    """Base class for all metamodel relationships.

    A relationship connects one source entity to one target entity.
    Relationships do not carry traceability metadata.
    """

    source_type: type[BaseEntity] | None = None
    target_type: type[BaseEntity] | None = None
    source_cardinality: str | None = None
    target_cardinality: str | None = None

    def __init__(self, source_entity: BaseEntity, target_entity: BaseEntity) -> None:
        self._id = str(uuid4())
        self._source_entity = self._validate_endpoint(source_entity, self.source_type, "source")
        self._target_entity = self._validate_endpoint(target_entity, self.target_type, "target")

    @staticmethod
    def _validate_endpoint(entity: BaseEntity, expected_type: type[BaseEntity] | None, role: str) -> BaseEntity:
        if expected_type is None:
            raise TypeError(f"{role}_type is not defined")
        if not isinstance(entity, expected_type):
            raise TypeError(f"{role}_entity must be an instance of {expected_type.__name__}")
        return entity

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def source_entity(self) -> BaseEntity:
        return self._source_entity

    @property
    def target_entity(self) -> BaseEntity:
        return self._target_entity

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "source": self.source_entity.id,
            "target": self.target_entity.id,
        }

    def __repr__(self) -> str:
        return f"{self.type}({self.source_entity!r} -> {self.target_entity!r})"
