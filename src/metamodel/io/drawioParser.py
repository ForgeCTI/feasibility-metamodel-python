from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from metamodel.core.Factory import Factory
from metamodel.core.Model import Model
from metamodel.core.Registry import Registry


def _clean(value: str | None) -> str:
    return html.unescape(re.sub("<[^>]+>", "", value or "")).strip()


def loadDrawioScenario(path: str | Path) -> Model:
    """Parse a simple draw.io scenario diagram into a Model.

    Vertices whose labels match registered entity classes are instantiated.
    Edges whose labels match registered relationship classes or aliases are instantiated.
    """
    registry = Registry.load_default()
    factory = Factory(registry)
    model = Model()
    tree = ET.parse(path)
    root = tree.getroot()
    cells = {cell.get("id"): cell for cell in root.iter("mxCell")}
    entity_by_cell_id = {}

    for cell_id, cell in cells.items():
        if cell.get("vertex") == "1" and "edgeLabel" not in cell.get("style", ""):
            label = _clean(cell.get("value"))
            label = "InternationalBody" if label == "International Body" else label
            if label in registry.entity_classes:
                entity = factory.create_entity(label, name=label)
                model.add_entity(entity)
                entity_by_cell_id[cell_id] = entity

    labels_by_parent = {}
    for cell in root.iter("mxCell"):
        parent = cell.get("parent")
        label = _clean(cell.get("value"))
        if parent and label:
            labels_by_parent.setdefault(parent, []).append(label)

    for cell_id, cell in cells.items():
        if cell.get("edge") == "1" and cell.get("source") in entity_by_cell_id and cell.get("target") in entity_by_cell_id:
            source_entity = entity_by_cell_id[cell.get("source")]
            target_entity = entity_by_cell_id[cell.get("target")]
            labels = [label for label in labels_by_parent.get(cell_id, []) if not re.fullmatch(r"[0-9]+(\.\.[0-9*]+)?", label)]
            if not labels:
                continue
            label = labels[0]
            try:
                rel = factory.create_relationship_from_alias(label, source_entity, target_entity)
            except Exception:
                continue
            model.add_relationship(rel)

    return model
