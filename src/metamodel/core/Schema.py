"""Introspection of entity and relationship classes (attributes, types, labels).

Used by the importers to coerce untyped values (e.g. CSV cells), by the CLI
``schema`` command, and by the adapters.
"""
from __future__ import annotations

import inspect
import types
import typing
from functools import lru_cache

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.BaseRelationship import BaseRelationship

#: Simple value kinds used for coercion and documentation.
KINDS = ("str", "int", "float", "bool", "list", "dict", "entity", "any")


def _kind(annotation) -> str:
    origin = typing.get_origin(annotation)
    if origin in (typing.Union, types.UnionType):
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        return _kind(args[0]) if len(args) == 1 else "any"
    if origin in (list, tuple, set) or annotation in (list, tuple, set):
        return "list"
    if origin is dict or annotation is dict:
        return "dict"
    if isinstance(annotation, type) and issubclass(annotation, BaseEntity):
        return "entity"
    for kind, py in (("bool", bool), ("int", int), ("float", float), ("str", str)):
        if annotation is py:
            return kind
    return "any"


@lru_cache(maxsize=None)
def entity_attribute_kinds(cls: type[BaseEntity]) -> dict[str, str]:
    """Map each domain attribute of an entity class to its value kind."""
    kinds: dict[str, str] = {}
    for attr in cls._domain_attributes:
        prop = inspect.getattr_static(cls, attr, None)
        kind = "any"
        if isinstance(prop, property) and prop.fget is not None:
            try:
                kind = _kind(typing.get_type_hints(prop.fget).get("return"))
            except Exception:  # pragma: no cover - defensive
                kind = "any"
        kinds[attr] = kind
    return kinds


def relationship_attribute_kinds(cls: type[BaseRelationship]) -> dict[str, str]:
    """Map each attribute of a relationship class to its value kind."""
    return {name: ("entity" if name in cls._entity_attributes else "any") for name in cls._domain_attributes}


def entity_lineage(cls: type[BaseEntity]) -> list[str]:
    """Class names from the entity itself up to (excluding) BaseEntity."""
    return [c.__name__ for c in cls.__mro__ if isinstance(c, type) and issubclass(c, BaseEntity) and c is not BaseEntity]


def describe_entity(cls: type[BaseEntity]) -> dict:
    parent = cls.__mro__[1]
    return {
        "name": cls.__name__,
        "domain": cls.__module__.split(".")[1],
        "knowledge_class": cls.knowledge_class,
        "superclass": parent.__name__ if parent is not BaseEntity else None,
        "attributes": entity_attribute_kinds(cls),
    }


def describe_relationship(cls: type[BaseRelationship]) -> dict:
    return {
        "name": cls.__name__,
        "label": cls.get_label(),
        "source": cls.source_type.__name__ if cls.source_type else None,
        "target": cls.target_type.__name__ if cls.target_type else None,
        "source_cardinality": cls.source_cardinality,
        "target_cardinality": cls.target_cardinality,
        "attributes": {name: (cls._entity_attributes[name].__name__ if name in cls._entity_attributes else "any")
                       for name in cls._domain_attributes},
    }


def describe_registry(registry) -> dict:
    return {
        "entities": [describe_entity(c) for c in registry.get_entity_classes()],
        "relationships": [describe_relationship(c) for c in registry.get_relationship_classes()],
    }
