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

    def add(self, obj: BaseEntity | BaseRelationship) -> BaseEntity | BaseRelationship:
        """Add an entity or relationship to the model."""

        if isinstance(obj, BaseEntity):
            if obj.id in self._entities:
                raise ValueError(f"entity with id {obj.id} already exists.")
            self._entities[obj.id] = obj
            return obj
        if isinstance(obj, BaseRelationship):
            for rel in self._relationships:
                if rel.id == obj.id:
                    raise ValueError(f"relationship with id {obj.id} already exists.")
            if obj.source_entity.id not in self._entities:
                raise ValueError("relationship source_entity is not present in the model.")
            if obj.target_entity.id not in self._entities:
                raise ValueError("relationship target_entity is not present in the model.")
            for rel in self._relationships:
                if (
                    rel.type == obj.type
                    and rel.source_entity.id == obj.source_entity.id
                    and rel.target_entity.id == obj.target_entity.id
                ):
                    raise ValueError("relationship already exists between these entities.")
            self._relationships.append(obj)
            return obj
        raise TypeError("obj must be an instance of BaseEntity or BaseRelationship.")

    def remove(self, obj: BaseEntity | BaseRelationship) -> None:
        """Remove an entity or relationship from the model.

        Entities cannot be removed while incident relationships exist.
        """

        if isinstance(obj, BaseEntity):
            if obj.id not in self._entities:
                raise ValueError("entity does not belong to the model.")
            for rel in self._relationships:
                if rel.source_entity.id == obj.id or rel.target_entity.id == obj.id:
                    raise ValueError("entity has incident relationships.")
            del self._entities[obj.id]
            return
        if isinstance(obj, BaseRelationship):
            if obj not in self._relationships:
                raise ValueError("relationship does not belong to the model.")
            self._relationships.remove(obj)
            return
        raise TypeError("obj must be an instance of BaseEntity or BaseRelationship.")


    def update_relationship(
        self,
        relationship: BaseRelationship,
        source_entity: BaseEntity | None = None,
        target_entity: BaseEntity | None = None,
    ) -> None:
        """Update relationship endpoints while preserving model consistency."""

        if not isinstance(relationship, BaseRelationship):
            raise TypeError("relationship must be an instance of BaseRelationship.")
        if relationship not in self._relationships:
            raise ValueError("relationship does not belong to the model.")
        new_source = source_entity if source_entity is not None else relationship.source_entity
        new_target = target_entity if target_entity is not None else relationship.target_entity
        relationship._validate_endpoint(new_source, relationship.source_type, "source")
        relationship._validate_endpoint(new_target, relationship.target_type, "target")
        if new_source.id not in self._entities:
            raise ValueError("source_entity is not present in the model.")
        if new_target.id not in self._entities:
            raise ValueError("target_entity is not present in the model.")
        for rel in self._relationships:
            if rel is relationship:
                continue
            if (
                rel.type == relationship.type
                and rel.source_entity.id == new_source.id
                and rel.target_entity.id == new_target.id
            ):
                raise ValueError("relationship already exists between these entities.")
        relationship._update_endpoints(new_source, new_target)

    def get_entity(self, entity_id: str) -> BaseEntity:
        return self._entities[entity_id]

    def get_entities_by_type(self, entity_type: str) -> list[BaseEntity]:
        return [entity for entity in self.entities if entity.type == entity_type]

    def get_relationships_by_type(self, relationship_type: str) -> list[BaseRelationship]:
        return [rel for rel in self.relationships if rel.type == relationship_type]

    def to_dict(self) -> dict:
        return {
            "entities": [entity.to_dict() for entity in self.entities],
            "relationships": [relationship.to_dict() for relationship in self.relationships],
        }

    def validate(self):
        from metamodel.validation.modelValidator import validateModel
        return validateModel(self)
