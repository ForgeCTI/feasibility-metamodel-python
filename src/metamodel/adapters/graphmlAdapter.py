from __future__ import annotations

from metamodel.adapters.networkxAdapter import toNetworkx


def saveGraphML(model, path: str) -> None:
    try:
        import networkx as nx
    except ImportError as exc:
        raise ImportError("networkx is required. Install with: pip install cyber-feasibility-metamodel[networkx]") from exc
    graph = toNetworkx(model)
    nx.write_graphml(graph, path)
