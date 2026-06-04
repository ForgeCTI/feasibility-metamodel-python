from __future__ import annotations

from pathlib import Path


def saveYamlScenario(model, path: str | Path) -> None:
    try:
        import yaml
    except ImportError as exc:
        raise ImportError("PyYAML is required. Install with: pip install cyber-feasibility-metamodel[yaml]") from exc
    with Path(path).open("w", encoding="utf-8") as handle:
        yaml.safe_dump(model.to_dict(), handle, sort_keys=False)
