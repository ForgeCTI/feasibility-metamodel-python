from __future__ import annotations


def toNetworkx(model):
    try:
        import networkx as nx
    except ImportError as exc:
        raise ImportError("networkx is required. Install with: pip install cyber-feasibility-metamodel[networkx]") from exc

    graph = nx.MultiDiGraph()
    for entity in model.entities:
        data = entity.to_dict()
        node_id = data.pop("id")
        graph.add_node(node_id, **data)
    for rel in model.relationships:
        graph.add_edge(
            rel.source_entity.id,
            rel.target_entity.id,
            key=rel.id,
            id=rel.id,
            type=rel.type,
        )
    return graph


def fromNetworkx(graph):
    raise NotImplementedError("fromNetworkx is intentionally left for domain-specific imports.")
