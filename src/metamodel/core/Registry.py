from __future__ import annotations

from importlib import import_module

from metamodel.core.Exceptions import RegistryError
from metamodel.registry_data import (
    ENTITY_IMPORTS,
    LEGACY_ENTITY_TYPES,
    LEGACY_RELATIONSHIP_TYPES,
    RELATIONSHIP_ALIASES,
    RELATIONSHIP_IMPORTS,
)
from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.BaseRelationship import BaseRelationship


class Registry:
    """Registry of entity and relationship classes."""

    def __init__(self) -> None:
        self._entity_classes: dict[str, type] = {}
        self._relationship_classes: dict[str, type] = {}
        self._relationship_aliases: dict[tuple[str, str, str], str] = {}
        self._legacy_entity_types: dict[str, str] = {}
        self._legacy_relationship_types: dict[str, str] = {}

    @classmethod
    def load_default(cls) -> "Registry":
        registry = cls()
        for name, module_path, class_name in ENTITY_IMPORTS:
            module = import_module(module_path)
            entity_class = getattr(module, class_name)
            if not isinstance(entity_class, type) or not issubclass(entity_class, BaseEntity):
                raise RegistryError(f"{class_name} is not a subclass of BaseEntity")
            registry._entity_classes[name] = entity_class
        for name, module_path, class_name in RELATIONSHIP_IMPORTS:
            module = import_module(module_path)
            relationship_class = getattr(module, class_name)
            if not isinstance(relationship_class, type) or not issubclass(relationship_class, BaseRelationship):
                raise RegistryError(f"{class_name} is not a subclass of BaseRelationship")
            registry._relationship_classes[name] = relationship_class
        for source, label, target, relationship_name in RELATIONSHIP_ALIASES:
            registry._relationship_aliases[(source, label, target)] = relationship_name
        registry._legacy_entity_types = dict(LEGACY_ENTITY_TYPES)
        registry._legacy_relationship_types = dict(LEGACY_RELATIONSHIP_TYPES)
        return registry

    # entities -----------------------------------------------------------
    def get_entity_class(self, entity_type: str) -> type:
        try:
            return self._entity_classes[entity_type]
        except KeyError as exc:
            raise RegistryError(f"Unknown entity type: {entity_type}") from exc

    def get_entity_classes(self) -> list[type[BaseEntity]]:
        return list(self._entity_classes.values())

    def has_entity_type(self, entity_type: str) -> bool:
        return entity_type in self._entity_classes

    def canonical_entity_type(self, entity_type: str) -> str:
        """Map a legacy entity type name (e.g. ``Information``) to its current name."""
        return self._legacy_entity_types.get(entity_type, entity_type)

    # relationships ------------------------------------------------------
    def get_relationship_class(self, relationship_type: str) -> type:
        try:
            return self._relationship_classes[relationship_type]
        except KeyError as exc:
            raise RegistryError(f"Unknown relationship type: {relationship_type}") from exc

    def get_relationship_classes(self) -> list[type[BaseRelationship]]:
        return list(self._relationship_classes.values())

    def has_relationship_type(self, relationship_type: str) -> bool:
        return relationship_type in self._relationship_classes

    def canonical_relationship_type(self, relationship_type: str) -> str:
        """Map a legacy relationship class name (e.g. ``listensOn``) to its current name."""
        return self._legacy_relationship_types.get(relationship_type, relationship_type)

    def resolve_relationship_alias(self, source_type: str, label: str, target_type: str) -> str:
        """Resolve a metamodel label (e.g. ``protects``) to a relationship class name.

        Endpoint types are matched along the inheritance hierarchy, so that, e.g.,
        ``Node --hostsResource--> Data`` resolves to ``hostsResource`` (declared on Resource).
        """
        for source in self._lineage(source_type):
            for target in self._lineage(target_type):
                name = self._relationship_aliases.get((source, label, target))
                if name is not None:
                    return name
        raise RegistryError(f"Unknown relationship alias: {source_type} --{label}--> {target_type}")

    def _lineage(self, entity_type: str) -> list[str]:
        entity_type = self.canonical_entity_type(entity_type)
        cls = self._entity_classes.get(entity_type)
        if cls is None:
            return [entity_type]
        return [c.__name__ for c in cls.__mro__ if isinstance(c, type) and issubclass(c, BaseEntity) and c is not BaseEntity]

    def resolve_relationship_type(self, name: str, source_type: str | None = None, target_type: str | None = None) -> str:
        """Resolve a class name, a legacy class name, or a label (with endpoint types)."""
        name = self.canonical_relationship_type(name)
        if name in self._relationship_classes:
            return name
        if source_type is not None and target_type is not None:
            return self.resolve_relationship_alias(source_type, name, target_type)
        raise RegistryError(f"Unknown relationship type: {name}")
