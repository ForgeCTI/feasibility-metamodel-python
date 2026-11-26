"""CSV export (see ``metamodel.io.csvParser`` for the format)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

from metamodel.io.csvParser import ENTITIES_FILE, METADATA_FILE, RELATIONSHIPS_FILE
from metamodel.io.serialization import ENTITY_CORE_FIELDS, RELATIONSHIP_CORE_FIELDS, model_to_data


def _cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False) if value else ""
    return str(value)


def _write(path: Path, rows: list[dict], core: tuple[str, ...]) -> None:
    extra = sorted({key for row in rows for key in row} - set(core))
    fields = list(core) + extra
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: _cell(row.get(key)) for key in fields})


def saveCsvScenario(model, entities_csv: str | Path, relationships_csv: str | Path) -> None:
    data = model_to_data(model, include_none=False)
    _write(Path(entities_csv), data["entities"], ENTITY_CORE_FIELDS)
    _write(Path(relationships_csv), data["relationships"], RELATIONSHIP_CORE_FIELDS)


def saveCsvDirectory(model, directory: str | Path) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    saveCsvScenario(model, directory / ENTITIES_FILE, directory / RELATIONSHIPS_FILE)
    if model.metadata:
        (directory / METADATA_FILE).write_text(json.dumps(model.metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
