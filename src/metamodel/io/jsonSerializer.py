from __future__ import annotations

import json
from pathlib import Path


def saveJsonScenario(model, path: str | Path, *, indent: int = 2) -> None:
    with Path(path).open("w", encoding="utf-8") as handle:
        json.dump(model.to_dict(), handle, indent=indent)
