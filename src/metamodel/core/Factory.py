from __future__ import annotations

from metamodel.core.Registry import Registry


class Factory:
    """Creates entities and relationships from type names."""

    def __init__(self, registry: Registry | None = None) -> None:
        self.registry = registry or Registry.load_default()

    def create_entity(self, entity_type: str, **kwargs):
        kwargs.pop("id", None)
        kwargs.pop("type", None)
        cls = self.registry.get_entity_class(entity_type)
        return cls(**kwargs)

    def create_relationship(self, relationship_type: str, source_entity, target_entity):
        cls = self.registry.get_relationship_class(relationship_type)
        return cls(source_entity, target_entity)

    def create_relationship_from_alias(self, label: str, source_entity, target_entity):
        relationship_type = self.registry.resolve_relationship_alias(source_entity.type, label, target_entity.type)
        return self.create_relationship(relationship_type, source_entity, target_entity)
