"""GraphML export and import through NetworkX (lists and dicts are stored as JSON strings)."""
from __future__ import annotations

from metamodel.adapters.networkxAdapter import _nx, fromNetworkx, toNetworkx


def saveGraphML(model, path: str) -> None:
    nx = _nx()
    nx.write_graphml(toNetworkx(model, flatten=True), path)


def loadGraphML(path: str, *, strict: bool = True):
    nx = _nx()
    graph = nx.read_graphml(path, force_multigraph=True)
    return fromNetworkx(graph, strict=strict, coerce=True)
