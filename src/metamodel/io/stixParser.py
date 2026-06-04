"""Extensible STIX parser for the CTI Feasibility Metamodel.

This parser accepts all STIX Domain Objects and STIX Relationship Objects listed
in the official OASIS CTI STIX introduction. It also preserves common STIX
Cyber-observable Objects and Meta Objects as generic STIX entities.

The design is registry-based:

- object mappers are registered by STIX object type;
- relationship mappers are registered by STIX SRO type;
- native mappings can be added without changing the parser core;
- unsupported but recognized STIX objects are preserved as GenericStixObject.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json

from metamodel.core.Model import Model

from metamodel.io.stix.constants import STIX_EDGE_OBJECT_TYPES, STIX_OBJECT_TYPES
from metamodel.io.stix.mappers import (
    build_default_object_registry,
    build_default_relationship_registry,
)
from metamodel.io.stix.registry import (
    StixObjectMapperRegistry,
    StixParserContext,
    StixRelationshipMapperRegistry,
)


@dataclass
class StixParseResult:
    """Result returned by the STIX parser."""

    model: Model
    stix_to_entity_id: dict[str, str] = field(default_factory=dict)
    skipped_objects: list[dict[str, str]] = field(default_factory=list)
    skipped_relationships: list[dict[str, str]] = field(default_factory=list)


class StixParser:
    """Extensible STIX parser.

    Args:
        object_registry: Optional object mapper registry. If omitted, the
            default registry is used.
        relationship_registry: Optional relationship mapper registry. If
            omitted, the default registry is used.
        preserve_unknown_objects: If True, unknown STIX custom objects are
            preserved as generic objects when possible.
    """

    def __init__(
        self,
        object_registry: StixObjectMapperRegistry | None = None,
        relationship_registry: StixRelationshipMapperRegistry | None = None,
        preserve_unknown_objects: bool = True,
    ) -> None:
        self.object_registry = object_registry or build_default_object_registry()
        self.relationship_registry = (
            relationship_registry or build_default_relationship_registry()
        )
        self.preserve_unknown_objects = preserve_unknown_objects

    def register_object_mapper(self, stix_type: str, mapper) -> None:
        """Register or override a mapper for a STIX object type."""
        self.object_registry.register(stix_type, mapper)

    def register_relationship_mapper(self, sro_type: str, mapper) -> None:
        """Register or override a mapper for a STIX relationship object type."""
        self.relationship_registry.register(sro_type, mapper)

    def load_file(self, path: str | Path) -> StixParseResult:
        """Load a STIX JSON bundle from a file."""
        path = Path(path)

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return self.parse(data)

    def parse(self, data: dict[str, Any] | list[dict[str, Any]]) -> StixParseResult:
        """Parse STIX data and return a parse result."""
        objects = _extract_objects(data)

        model = Model()
        context = StixParserContext(model=model)

        # First pass: instantiate all node-like objects.
        for stix_object in objects:
            stix_type = stix_object.get("type")

            if stix_type in STIX_EDGE_OBJECT_TYPES:
                continue

            mapper = self.object_registry.get(stix_type)

            if mapper is None:
                if self.preserve_unknown_objects and isinstance(stix_type, str):
                    from metamodel.io.stix.mappers import map_generic_object

                    mapper = map_generic_object
                else:
                    context.skipped_objects.append(
                        {
                            "id": str(stix_object.get("id", "<missing-id>")),
                            "type": str(stix_type),
                            "reason": "no mapper registered for STIX object type",
                        }
                    )
                    continue

            try:
                entity = mapper(stix_object, context)
            except Exception as exc:
                context.skipped_objects.append(
                    {
                        "id": str(stix_object.get("id", "<missing-id>")),
                        "type": str(stix_type),
                        "reason": f"mapper error: {exc}",
                    }
                )
                continue

            if entity is None:
                context.skipped_objects.append(
                    {
                        "id": str(stix_object.get("id", "<missing-id>")),
                        "type": str(stix_type),
                        "reason": "mapper returned None",
                    }
                )
                continue

            model.add_entity(entity)

            stix_id = stix_object.get("id")
            if isinstance(stix_id, str):
                context.stix_to_entity[stix_id] = entity
                context.stix_to_entity_id[stix_id] = entity.id

        # Second pass: instantiate edge-like objects.
        for stix_object in objects:
            stix_type = stix_object.get("type")

            if stix_type not in STIX_EDGE_OBJECT_TYPES:
                continue

            mapper = self.relationship_registry.get(stix_type)

            if mapper is None:
                context.skipped_relationships.append(
                    {
                        "id": str(stix_object.get("id", "<missing-id>")),
                        "type": str(stix_type),
                        "reason": "no mapper registered for STIX relationship object type",
                    }
                )
                continue

            try:
                relationships = mapper(stix_object, context)
            except Exception as exc:
                context.skipped_relationships.append(
                    {
                        "id": str(stix_object.get("id", "<missing-id>")),
                        "type": str(stix_type),
                        "reason": f"relationship mapper error: {exc}",
                    }
                )
                continue

            for relationship in relationships:
                model.add_relationship(relationship)

        return StixParseResult(
            model=model,
            stix_to_entity_id=context.stix_to_entity_id,
            skipped_objects=context.skipped_objects,
            skipped_relationships=context.skipped_relationships,
        )


def loadStixBundle(path: str | Path) -> Model:
    """Load a STIX JSON bundle and return a Model."""
    return loadStixBundleWithReport(path).model


def loadStixBundleWithReport(path: str | Path) -> StixParseResult:
    """Load a STIX JSON bundle and return a parse result."""
    return StixParser().load_file(path)


def parseStixBundle(data: dict[str, Any] | list[dict[str, Any]]) -> Model:
    """Parse STIX data and return a Model."""
    return parseStixBundleWithReport(data).model


def parseStixBundleWithReport(
    data: dict[str, Any] | list[dict[str, Any]],
) -> StixParseResult:
    """Parse STIX data and return a parse result."""
    return StixParser().parse(data)


def _extract_objects(data: dict[str, Any] | list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Extract STIX objects from either a bundle dict or a raw object list."""
    if isinstance(data, list):
        objects = data
    elif isinstance(data, dict):
        if data.get("type") == "bundle":
            objects = data.get("objects", [])
        elif "objects" in data:
            objects = data.get("objects", [])
        else:
            objects = [data]
    else:
        raise TypeError("STIX data must be a dictionary or a list of dictionaries.")

    if not isinstance(objects, list):
        raise ValueError("STIX bundle 'objects' must be a list.")

    clean_objects = []
    for obj in objects:
        if not isinstance(obj, dict):
            raise ValueError("Every STIX object must be a dictionary.")
        clean_objects.append(obj)

    return clean_objects
