from __future__ import annotations

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.BaseRelationship import BaseRelationship


class Model:
    """Container for a metamodel scenario."""

    def __init__(self) -> None:
        self._entities: dict[str, BaseEntity] = {}
        self._relationships: list[BaseRelationship] = []

    @property
    def entities(self) -> list[BaseEntity]:
        return list(self._entities.values())

    @property
    def relationships(self) -> list[BaseRelationship]:
        return list(self._relationships)

    def add_entity(self, entity: BaseEntity) -> BaseEntity:
        if not isinstance(entity, BaseEntity):
            raise TypeError("entity must be an instance of BaseEntity.")
        if entity.id in self._entities:
            raise ValueError(f"entity with id {entity.id} already exists.")
        self._entities[entity.id] = entity
        return entity

    def add_relationship(self, relationship: BaseRelationship) -> BaseRelationship:
        if not isinstance(relationship, BaseRelationship):
            raise TypeError("relationship must be an instance of BaseRelationship.")
        if relationship.source_entity.id not in self._entities:
            raise ValueError("relationship source_entity is not present in the model.")
        if relationship.target_entity.id not in self._entities:
            raise ValueError("relationship target_entity is not present in the model.")
        self._relationships.append(relationship)
        return relationship

    def get_entity(self, entity_id: str) -> BaseEntity:
        return self._entities[entity_id]

    def entities_by_type(self, entity_type: str) -> list[BaseEntity]:
        return [entity for entity in self.entities if entity.type == entity_type]

    def relationships_by_type(self, relationship_type: str) -> list[BaseRelationship]:
        return [rel for rel in self.relationships if rel.type == relationship_type]

    def to_dict(self) -> dict:
        return {
            "entities": [entity.to_dict() for entity in self.entities],
            "relationships": [relationship.to_dict() for relationship in self.relationships],
        }

    def validate(self):
        from metamodel.validation.modelValidator import validateModel
        return validateModel(self)
