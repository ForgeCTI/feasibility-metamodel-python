"""Load and save models by format name or file extension.

Formats: ``json``, ``yaml``, ``csv`` (a directory with ``entities.csv`` and
``relationships.csv``), ``graphml``, ``cypher`` (export only), ``stix``
(import only), ``drawio`` (import only).
"""
from __future__ import annotations

from pathlib import Path

FORMATS_IN = ("json", "yaml", "csv", "graphml", "stix", "drawio")
FORMATS_OUT = ("json", "yaml", "csv", "graphml", "cypher")


def detect_format(path: str | Path) -> str:
    path = Path(path)
    if path.is_dir() or path.suffix == "":
        return "csv"
    suffix = path.suffix.lower()
    name = path.name.lower()
    if suffix in (".yaml", ".yml"):
        return "yaml"
    if suffix == ".csv":
        return "csv"
    if suffix == ".graphml":
        return "graphml"
    if suffix in (".cypher", ".cql"):
        return "cypher"
    if suffix in (".drawio",) or name.endswith(".drawio.xml"):
        return "drawio"
    if suffix == ".json":
        return "json"
    raise ValueError(f"cannot detect the format of {path}; pass it explicitly.")


def loadModel(path: str | Path, fmt: str | None = None, *, strict: bool = True):
    """Load a model from a file (or CSV directory)."""
    fmt = fmt or detect_format(path)
    if fmt == "json":
        from metamodel.io.jsonParser import loadJsonScenario
        return loadJsonScenario(path, strict=strict)
    if fmt == "yaml":
        from metamodel.io.yamlParser import loadYamlScenario
        return loadYamlScenario(path, strict=strict)
    if fmt == "csv":
        from metamodel.io.csvParser import loadCsvDirectory
        path = Path(path)
        return loadCsvDirectory(path if path.is_dir() else path.parent, strict=strict)
    if fmt == "graphml":
        from metamodel.adapters.graphmlAdapter import loadGraphML
        return loadGraphML(path)
    if fmt == "stix":
        from metamodel.io.stixParser import loadStixBundle
        return loadStixBundle(path)
    if fmt == "drawio":
        from metamodel.io.drawioParser import loadDrawioScenario
        return loadDrawioScenario(path)
    raise ValueError(f"unsupported input format {fmt!r}; expected one of {', '.join(FORMATS_IN)}.")


def saveModel(model, path: str | Path, fmt: str | None = None) -> None:
    """Save a model to a file (or CSV directory)."""
    fmt = fmt or detect_format(path)
    if fmt == "json":
        from metamodel.io.jsonSerializer import saveJsonScenario
        return saveJsonScenario(model, path)
    if fmt == "yaml":
        from metamodel.io.yamlSerializer import saveYamlScenario
        return saveYamlScenario(model, path)
    if fmt == "csv":
        from metamodel.io.csvSerializer import saveCsvDirectory
        path = Path(path)
        return saveCsvDirectory(model, path.parent if path.suffix.lower() == ".csv" else path)
    if fmt == "graphml":
        from metamodel.adapters.graphmlAdapter import saveGraphML
        return saveGraphML(model, str(path))
    if fmt == "cypher":
        from metamodel.adapters.neo4jAdapter import toCypherScript
        Path(path).write_text(toCypherScript(model), encoding="utf-8")
        return None
    raise ValueError(f"unsupported output format {fmt!r}; expected one of {', '.join(FORMATS_OUT)}.")
