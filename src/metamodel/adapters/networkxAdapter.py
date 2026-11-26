"""NetworkX adapter.

``toNetworkx`` returns a ``MultiDiGraph`` whose nodes are entities (key: entity
id) and whose edges are relationships (key: relationship id).

Node attributes: ``type``, ``labels`` (the type and its superclasses, e.g.
``["ApplicationInstance", "Code", "Resource"]``), ``knowledge_class``, ``name``,
``description``, ``source``, and the domain attributes of the entity.
Edge attributes: ``id``, ``type`` (relationship class), ``label`` (metamodel
label, e.g. ``grantsAccessTo``), and relationship attributes (entity-valued
attributes hold entity ids). Scenario metadata is stored in ``graph.graph``.

``fromNetworkx`` performs the inverse conversion; nodes and edges must carry a
``type`` attribute (edges may carry only ``label``).
"""
from __future__ import annotations

import json

from metamodel.core.Schema import entity_lineage
from metamodel.io.serialization import data_to_model

DERIVED_NODE_ATTRIBUTES = ("labels", "knowledge_class")
DERIVED_EDGE_ATTRIBUTES = ("label",)


def _nx():
    try:
        import networkx as nx
    except ImportError as exc:
        raise ImportError("networkx is required. Install with: pip install cti-feasibility-metamodel[networkx]") from exc
    return nx


def _flat(value):
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    return value


def toNetworkx(model, *, flatten: bool = False, include_none: bool = False):
    """Convert a model to a NetworkX ``MultiDiGraph``.

    Args:
        flatten: encode lists and dicts as JSON strings (required by GraphML).
        include_none: keep attributes whose value is ``None``.
    """
    nx = _nx()
    graph = nx.MultiDiGraph()
    if model.metadata:
        graph.graph.update({k: (_flat(v) if flatten else v) for k, v in model.metadata.items()})
    for entity in model.entities:
        data = entity.to_dict()
        node_id = data.pop("id")
        data["labels"] = entity_lineage(type(entity))
        data["knowledge_class"] = entity.knowledge_class
        data = {k: v for k, v in data.items() if include_none or (v is not None and v != [])}
        if flatten:
            data = {k: _flat(v) for k, v in data.items()}
        graph.add_node(node_id, **data)
    for rel in model.relationships:
        data = rel.to_dict()
        data.pop("source")
        data.pop("target")
        data["label"] = rel.get_label()
        data = {k: v for k, v in data.items() if include_none or v is not None}
        if flatten:
            data = {k: _flat(v) for k, v in data.items()}
        graph.add_edge(rel.source_entity.id, rel.target_entity.id, key=rel.id, **data)
    return graph


def fromNetworkx(graph, *, strict: bool = True, coerce: bool = False):
    """Convert a NetworkX graph produced by ``toNetworkx`` (or compatible) to a model."""
    entities = []
    for node_id, attrs in graph.nodes(data=True):
        item = {k: v for k, v in attrs.items() if k not in DERIVED_NODE_ATTRIBUTES}
        item["id"] = str(node_id)
        entities.append(item)
    relationships = []
    edges = graph.edges(keys=True, data=True) if graph.is_multigraph() else ((u, v, None, d) for u, v, d in graph.edges(data=True))
    for source, target, key, attrs in edges:
        item = {k: v for k, v in attrs.items() if k not in DERIVED_EDGE_ATTRIBUTES}
        item.setdefault("type", attrs.get("label"))
        if key is not None and not isinstance(key, int):
            item.setdefault("id", str(key))
        item["source"] = str(source)
        item["target"] = str(target)
        relationships.append(item)
    metadata = {}
    for k, v in dict(graph.graph).items():
        if k in ("node_default", "edge_default"):  # added by the GraphML reader
            continue
        if isinstance(v, str) and v[:1] in "[{":
            try:
                v = json.loads(v)
            except ValueError:
                pass
        metadata[k] = v
    data = {"metadata": metadata, "entities": entities, "relationships": relationships}
    return data_to_model(data, strict=strict, coerce=coerce).model
