"""Format-independent conversion between a Model and plain data.

The scenario data format is shared by JSON, YAML, CSV, NetworkX, and Neo4j:

.. code-block:: yaml

    metadata: {name: ..., completeness: [Node, Account]}   # optional
    entities:
      - {id: n1, type: Node, name: Mail server, hostname: mx1}
    relationships:
      - {id: r1, type: grantsAccessTo, source: acc1, target: n1, privilege_level: admin}

* ``id`` values are preserved on import, so a model can be exported and
  re-imported without changing identifiers. Missing ids are generated.
* A relationship ``type`` may be the class name (``grantsAccessToNode``), the
  metamodel label (``grantsAccessTo``, resolved from the endpoint types), or a
  legacy name (``listensOn``); legacy entity types (``Information``) are mapped too.
* Entity-valued relationship attributes (``privilege_level``) hold entity ids.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.Exceptions import ParseError, RegistryError
from metamodel.core.Factory import Factory
from metamodel.core.Model import Model
from metamodel.core.Schema import entity_attribute_kinds

ENTITY_CORE_FIELDS = ("id", "type", "name", "description", "source")
RELATIONSHIP_CORE_FIELDS = ("id", "type", "source", "target")


@dataclass
class ParseResult:
    model: Model
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------- export
def model_to_data(model: Model, *, include_none: bool = True, include_label: bool = False) -> dict:
    """Convert a model to the scenario data format."""
    entities = []
    for entity in model.entities:
        item = entity.to_dict()
        entities.append(item if include_none else {k: v for k, v in item.items() if v is not None and v != []})
    relationships = []
    for rel in model.relationships:
        item = rel.to_dict()
        if include_label:
            item["label"] = rel.get_label()
        relationships.append(item if include_none else {k: v for k, v in item.items() if v is not None})
    data: dict[str, Any] = {}
    if model.metadata:
        data["metadata"] = dict(model.metadata)
    data["entities"] = entities
    data["relationships"] = relationships
    return data


# ---------------------------------------------------------------- import
def coerce_value(value: Any, kind: str) -> Any:
    """Coerce a textual value (e.g. a CSV cell) to the expected attribute kind."""
    if not isinstance(value, str):
        return value
    text = value.strip()
    if text == "":
        return None
    if kind == "str" or kind == "entity":
        return value
    if kind == "bool":
        lowered = text.lower()
        if lowered in ("true", "yes", "1"):
            return True
        if lowered in ("false", "no", "0"):
            return False
        raise ValueError(f"cannot interpret {value!r} as a boolean")
    if kind == "int":
        return int(text)
    if kind == "float":
        return float(text)
    if kind in ("list", "dict", "any"):
        if text[0] in "[{":
            return json.loads(text)
        if kind == "list":
            return [item.strip() for item in text.split(";") if item.strip()]
        return value
    return value


def data_to_model(
    data: dict,
    *,
    factory: Factory | None = None,
    strict: bool = True,
    coerce: bool = False,
) -> ParseResult:
    """Convert scenario data to a model.

    Args:
        strict: raise ``ParseError`` on unknown types or attributes; when false,
            skip them and report a warning.
        coerce: convert textual values to the attribute types (used for CSV).
    """
    if not isinstance(data, dict):
        raise ParseError("scenario data must be a mapping with 'entities' and 'relationships'.")
    factory = factory or Factory()
    registry = factory.registry
    model = Model()
    model.metadata = dict(data.get("metadata") or {})
    warnings: list[str] = []
    refs: dict[str, BaseEntity] = {}

    def problem(message: str) -> None:
        if strict:
            raise ParseError(message)
        warnings.append(message)

    for index, raw in enumerate(data.get("entities") or []):
        item = {k: v for k, v in dict(raw).items() if v is not None}
        raw_type = item.pop("type", None)
        if raw_type is None:
            problem(f"entity #{index} has no type.")
            continue
        entity_type = registry.canonical_entity_type(raw_type)
        if entity_type != raw_type:
            warnings.append(f"entity type {raw_type!r} is deprecated; using {entity_type!r}.")
        ref = item.pop("id", None) or item.pop("ref", None)
        if not registry.has_entity_type(entity_type):
            problem(f"entity {ref or index!r}: unknown type {raw_type!r}.")
            continue
        cls = registry.get_entity_class(entity_type)
        kinds = entity_attribute_kinds(cls)
        allowed = set(kinds) | {"name", "description", "source"}
        unknown = sorted(set(item) - allowed)
        if unknown:
            problem(f"entity {ref or index!r} ({entity_type}): unknown attribute(s) {', '.join(unknown)}.")
            for key in unknown:
                item.pop(key)
        try:
            if coerce:
                item = {k: coerce_value(v, kinds.get(k, "str")) for k, v in item.items()}
                item = {k: v for k, v in item.items() if v is not None}
            entity = factory.create_entity(entity_type, **item)
        except (TypeError, ValueError) as exc:
            raise ParseError(f"entity {ref or index!r} ({entity_type}): {exc}") from exc
        if ref is not None:
            ref = str(ref)
            if ref in refs:
                raise ParseError(f"duplicate entity id {ref!r}.")
            entity._restore_id(ref)
            refs[ref] = entity
        model.add(entity)
        refs.setdefault(entity.id, entity)

    for index, raw in enumerate(data.get("relationships") or []):
        item = {k: v for k, v in dict(raw).items() if v is not None}
        item.pop("label", None)
        raw_type = item.pop("type", None)
        rel_ref = item.pop("id", None)
        try:
            source = refs[str(item.pop("source"))]
            target = refs[str(item.pop("target"))]
        except KeyError as exc:
            problem(f"relationship {rel_ref or index!r}: unknown or missing endpoint {exc}.")
            continue
        if raw_type is None:
            problem(f"relationship {rel_ref or index!r} has no type.")
            continue
        try:
            rel_type = registry.resolve_relationship_type(str(raw_type), source.type, target.type)
        except RegistryError as exc:
            problem(f"relationship {rel_ref or index!r}: {exc}")
            continue
        cls = registry.get_relationship_class(rel_type)
        unknown = sorted(set(item) - set(cls._domain_attributes))
        if unknown:
            problem(f"relationship {rel_ref or index!r} ({rel_type}): unknown attribute(s) {', '.join(unknown)}.")
            for key in unknown:
                item.pop(key)
        for name in cls._entity_attributes:
            if name in item:
                value = item[name]
                if isinstance(value, str) and value.strip() == "":
                    item.pop(name)
                    continue
                if str(value) not in refs:
                    raise ParseError(f"relationship {rel_ref or index!r}: {name} refers to unknown entity {value!r}.")
                item[name] = refs[str(value)]
        try:
            rel = factory.create_relationship(rel_type, source, target, **item)
        except (TypeError, ValueError) as exc:
            raise ParseError(f"relationship {rel_ref or index!r} ({rel_type}): {exc}") from exc
        if rel_ref is not None:
            rel._restore_id(str(rel_ref))
        try:
            model.add(rel)
        except ValueError as exc:
            problem(f"relationship {rel_ref or index!r} ({rel_type}): {exc}")
    return ParseResult(model, warnings)
