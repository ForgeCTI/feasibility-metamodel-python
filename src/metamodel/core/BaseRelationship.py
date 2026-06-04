from __future__ import annotations

from uuid import uuid4


class BaseRelationship:
    """Base class for all metamodel relationships.

    A relationship connects one source entity to one target entity.
    Relationships do not carry traceability metadata.
    """

    source_type = None
    target_type = None
    source_cardinality: str | None = None
    target_cardinality: str | None = None

    def __init__(self, source_entity, target_entity) -> None:
        self._id = str(uuid4())
        self._source_entity = None
        self._target_entity = None
        self.source_entity = source_entity
        self.target_entity = target_entity

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def source_entity(self):
        return self._source_entity

    @source_entity.setter
    def source_entity(self, value) -> None:
        if self.source_type is not None and not isinstance(value, self.source_type):
            raise TypeError(
                f"{self.type} source_entity must be an instance of {self.source_type.__name__}."
            )
        self._source_entity = value

    @property
    def target_entity(self):
        return self._target_entity

    @target_entity.setter
    def target_entity(self, value) -> None:
        if self.target_type is not None and not isinstance(value, self.target_type):
            raise TypeError(
                f"{self.type} target_entity must be an instance of {self.target_type.__name__}."
            )
        self._target_entity = value

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type,
            "source": self.source_entity.id,
            "target": self.target_entity.id,
        }

    def __repr__(self) -> str:
        return f"{self.type}({self.source_entity!r} -> {self.target_entity!r})"
