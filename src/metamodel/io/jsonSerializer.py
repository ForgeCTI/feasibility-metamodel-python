from __future__ import annotations

import json
from pathlib import Path

from metamodel.io.serialization import model_to_data


def dumpsJsonScenario(model, *, indent: int | None = 2, include_none: bool = False) -> str:
    return json.dumps(model_to_data(model, include_none=include_none), indent=indent, ensure_ascii=False)


def saveJsonScenario(model, path: str | Path, *, indent: int = 2, include_none: bool = False) -> None:
    Path(path).write_text(dumpsJsonScenario(model, indent=indent, include_none=include_none) + "\n", encoding="utf-8")
