from __future__ import annotations

import csv
from pathlib import Path

from metamodel.io.jsonParser import parseScenario


def loadCsvScenario(entities_csv: str | Path, relationships_csv: str | Path):
    entities = []
    relationships = []
    with Path(entities_csv).open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            entities.append({key: value for key, value in row.items() if value not in (None, "")})
    with Path(relationships_csv).open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            relationships.append({key: value for key, value in row.items() if value not in (None, "")})
    return parseScenario({"entities": entities, "relationships": relationships})
