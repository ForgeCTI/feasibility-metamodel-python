from __future__ import annotations

import json
from pathlib import Path

from metamodel.core.Factory import Factory
from metamodel.core.Model import Model


def parseScenario(data: dict, *, factory: Factory | None = None) -> Model:
    factory = factory or Factory()
    model = Model()
    external_ids = {}

    for index, raw_entity in enumerate(data.get("entities", [])):
        entity_data = dict(raw_entity)
        entity_type = entity_data.pop("type")
        external_id = entity_data.pop("id", None) or entity_data.pop("ref", None) or f"entity-{index}"
        entity = factory.create_entity(entity_type, **entity_data)
        model.add_entity(entity)
        external_ids[external_id] = entity
        external_ids[entity.id] = entity

    for raw_relationship in data.get("relationships", []):
        relationship_data = dict(raw_relationship)
        relationship_type = relationship_data.pop("type")
        relationship_data.pop("id", None)
        source_ref = relationship_data.pop("source")
        target_ref = relationship_data.pop("target")
        source = external_ids[source_ref]
        target = external_ids[target_ref]
        relationship = factory.create_relationship(relationship_type, source, target)
        model.add_relationship(relationship)

    return model


def loadJsonScenario(path: str | Path) -> Model:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return parseScenario(data)
