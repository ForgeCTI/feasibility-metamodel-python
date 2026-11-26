from __future__ import annotations

from pathlib import Path

from metamodel.io.jsonParser import parseScenario


def _yaml():
    try:
        import yaml
    except ImportError as exc:
        raise ImportError("PyYAML is required. Install with: pip install cti-feasibility-metamodel[yaml]") from exc
    return yaml


def loadsYamlScenario(text: str, *, strict: bool = True):
    return parseScenario(_yaml().safe_load(text), strict=strict)


def loadYamlScenario(path: str | Path, *, strict: bool = True):
    with Path(path).open("r", encoding="utf-8") as handle:
        data = _yaml().safe_load(handle)
    return parseScenario(data, strict=strict)
