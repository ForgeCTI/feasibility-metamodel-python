from __future__ import annotations

from pathlib import Path

from metamodel.io.jsonParser import parseScenario


def loadYamlScenario(path: str | Path):
    try:
        import yaml
    except ImportError as exc:
        raise ImportError("PyYAML is required. Install with: pip install cyber-feasibility-metamodel[yaml]") from exc
    with Path(path).open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return parseScenario(data)
