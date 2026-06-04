from __future__ import annotations

from importlib import import_module

from metamodel.core.Exceptions import RegistryError
from metamodel.registry_data import ENTITY_IMPORTS, RELATIONSHIP_ALIASES, RELATIONSHIP_IMPORTS


class Registry:
    """Registry of entity and relationship classes."""

    def __init__(self) -> None:
        self.entity_classes: dict[str, type] = {}
        self.relationship_classes: dict[str, type] = {}
        self.relationship_aliases: dict[tuple[str, str, str], str] = {}

    @classmethod
    def load_default(cls) -> "Registry":
        registry = cls()
        for name, module_path, class_name in ENTITY_IMPORTS:
            module = import_module(module_path)
            registry.entity_classes[name] = getattr(module, class_name)
        for name, module_path, class_name in RELATIONSHIP_IMPORTS:
            module = import_module(module_path)
            registry.relationship_classes[name] = getattr(module, class_name)
        for source, label, target, relationship_name in RELATIONSHIP_ALIASES:
            registry.relationship_aliases[(source, label, target)] = relationship_name
        return registry

    def get_entity_class(self, entity_type: str) -> type:
        try:
            return self.entity_classes[entity_type]
        except KeyError as exc:
            raise RegistryError(f"Unknown entity type: {entity_type}") from exc

    def get_relationship_class(self, relationship_type: str) -> type:
        try:
            return self.relationship_classes[relationship_type]
        except KeyError as exc:
            raise RegistryError(f"Unknown relationship type: {relationship_type}") from exc

    def resolve_relationship_alias(self, source_type: str, label: str, target_type: str) -> str:
        try:
            return self.relationship_aliases[(source_type, label, target_type)]
        except KeyError as exc:
            raise RegistryError(
                f"Unknown relationship alias: {source_type} --{label}--> {target_type}"
            ) from exc
