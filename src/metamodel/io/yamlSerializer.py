from __future__ import annotations

from pathlib import Path

from metamodel.io.serialization import model_to_data
from metamodel.io.yamlParser import _yaml


def dumpsYamlScenario(model, *, include_none: bool = False) -> str:
    return _yaml().safe_dump(model_to_data(model, include_none=include_none), sort_keys=False, allow_unicode=True)


def saveYamlScenario(model, path: str | Path, *, include_none: bool = False) -> None:
    Path(path).write_text(dumpsYamlScenario(model, include_none=include_none), encoding="utf-8")
