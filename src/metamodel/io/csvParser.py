"""CSV import.

A scenario is stored as two files: ``entities.csv`` (columns ``id``, ``type``,
``name``, ``description``, ``source``, then one column per attribute) and
``relationships.csv`` (columns ``id``, ``type``, ``source``, ``target``, then one
column per relationship attribute). Empty cells mean "not set". Cells are
converted to the attribute types: booleans (``true``/``false``), numbers, and
lists/dicts written as JSON (``["10.0.0.1"]``) or, for lists, separated by ``;``.
An optional ``metadata.json`` next to the files is read as scenario metadata.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from metamodel.io.serialization import data_to_model

ENTITIES_FILE = "entities.csv"
RELATIONSHIPS_FILE = "relationships.csv"
METADATA_FILE = "metadata.json"


def _rows(path: str | Path) -> list[dict]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [{k: v for k, v in row.items() if k and v not in (None, "")} for row in csv.DictReader(handle)]


def loadCsvScenario(entities_csv: str | Path, relationships_csv: str | Path, *, strict: bool = True, metadata: dict | None = None):
    data = {"metadata": metadata or {}, "entities": _rows(entities_csv), "relationships": _rows(relationships_csv)}
    return data_to_model(data, strict=strict, coerce=True).model


def loadCsvDirectory(directory: str | Path, *, strict: bool = True):
    directory = Path(directory)
    meta_path = directory / METADATA_FILE
    metadata = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else None
    return loadCsvScenario(directory / ENTITIES_FILE, directory / RELATIONSHIPS_FILE, strict=strict, metadata=metadata)
