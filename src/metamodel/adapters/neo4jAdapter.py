"""Neo4j adapter.

Graph layout in Neo4j:

* every entity is a node with label ``Entity`` plus one label per class in its
  hierarchy, e.g. ``(:Entity:ApplicationInstance:Code:Resource)``, so that
  queries can match supertypes (``MATCH (r:Resource)``); properties are ``id``,
  ``type``, ``knowledge_class``, ``name``, ``description``, ``source``, and the
  domain attributes (dicts are stored as JSON strings);
* every relationship has the metamodel label as relationship type (e.g.
  ``grantsAccessTo``, ``protects``, ``instanceOf``) and properties ``id``,
  ``class`` (the Python class, e.g. ``grantsAccessToNode``), and its attributes.
  For ``grantsAccessTo``, ``privilege_level`` holds the id of the PrivilegeLevel
  entity and the derived properties ``privilege_level_name`` and
  ``privilege_level_rank`` allow comparisons in queries.

``toCypherStatements`` produces parameterized, batched statements;
``toCypherScript`` produces a self-contained script for ``cypher-shell``;
``exportToNeo4j`` and ``importFromNeo4j`` use the official driver.
"""
from __future__ import annotations

import json
import math
import re
from collections import defaultdict

from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.Schema import entity_lineage
from metamodel.io.serialization import data_to_model

ENTITY_LABEL = "Entity"
CONSTRAINT = f"CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (n:{ENTITY_LABEL}) REQUIRE n.id IS UNIQUE"
DERIVED_NODE_PROPERTIES = ("knowledge_class",)
DERIVED_EDGE_PROPERTIES = ("class", "privilege_level_name", "privilege_level_rank")
_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _ident(name: str) -> str:
    if not _IDENT.match(name):
        raise ValueError(f"invalid Neo4j identifier: {name!r}")
    return f"`{name}`"


def _prop(value):
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return value


def _node_rows(model):
    groups = defaultdict(list)
    for entity in model.entities:
        props = {k: _prop(v) for k, v in entity.to_dict().items() if v is not None and v != [] and k != "id"}
        props["knowledge_class"] = entity.knowledge_class
        props = {k: v for k, v in props.items() if v is not None}
        groups[tuple(entity_lineage(type(entity)))].append({"id": entity.id, "props": props})
    return groups


def _edge_rows(model):
    groups = defaultdict(list)
    for rel in model.relationships:
        props = {"class": rel.type}
        for name, value in rel.attributes.items():
            if value is None:
                continue
            if isinstance(value, BaseEntity):
                props[name] = value.id
                props[f"{name}_name"] = value.name
                rank = getattr(value, "rank", None)
                if rank is not None:
                    props[f"{name}_rank"] = rank
            else:
                props[name] = _prop(value)
        groups[rel.get_label()].append({
            "id": rel.id, "source": rel.source_entity.id, "target": rel.target_entity.id, "props": props,
        })
    return groups


def _batches(rows, size):
    for start in range(0, len(rows), size):
        yield rows[start:start + size]


def toCypherStatements(model, *, batch_size: int = 500, clear: bool = False) -> list[tuple[str, dict]]:
    """Parameterized Cypher statements (query, parameters) that load the model into Neo4j."""
    statements: list[tuple[str, dict]] = []
    if clear:
        statements.append((f"MATCH (n:{ENTITY_LABEL}) DETACH DELETE n", {}))
    statements.append((CONSTRAINT, {}))
    for labels, rows in _node_rows(model).items():
        extra = ":".join(_ident(label) for label in labels)
        query = (f"UNWIND $rows AS row MERGE (n:{ENTITY_LABEL} {{id: row.id}}) "
                 f"SET n:{extra} SET n += row.props")
        statements.extend((query, {"rows": batch}) for batch in _batches(rows, batch_size))
    for label, rows in _edge_rows(model).items():
        query = (f"UNWIND $rows AS row "
                 f"MATCH (a:{ENTITY_LABEL} {{id: row.source}}), (b:{ENTITY_LABEL} {{id: row.target}}) "
                 f"MERGE (a)-[r:{_ident(label)} {{id: row.id}}]->(b) SET r += row.props")
        statements.extend((query, {"rows": batch}) for batch in _batches(rows, batch_size))
    return statements


def cypher_literal(value) -> str:
    """Format a Python value as a Cypher literal."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite floats cannot be stored in Neo4j")
        return repr(value)
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(cypher_literal(v) for v in value) + "]"
    if isinstance(value, dict):
        return "{" + ", ".join(f"{_ident(k)}: {cypher_literal(v)}" for k, v in value.items()) + "}"
    text = str(value).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")
    return f"'{text}'"


def toCypherScript(model, *, clear: bool = False) -> str:
    """A self-contained Cypher script (one statement per line) for ``cypher-shell`` or Neo4j Browser."""
    lines = ["// Generated by cti-feasibility-metamodel"]
    if clear:
        lines.append(f"MATCH (n:{ENTITY_LABEL}) DETACH DELETE n;")
    lines.append(CONSTRAINT + ";")
    for labels, rows in _node_rows(model).items():
        extra = ":".join(_ident(label) for label in labels)
        for row in rows:
            lines.append(f"MERGE (n:{ENTITY_LABEL} {{id: {cypher_literal(row['id'])}}}) "
                         f"SET n:{extra} SET n += {cypher_literal(row['props'])};")
    for label, rows in _edge_rows(model).items():
        for row in rows:
            lines.append(
                f"MATCH (a:{ENTITY_LABEL} {{id: {cypher_literal(row['source'])}}}), "
                f"(b:{ENTITY_LABEL} {{id: {cypher_literal(row['target'])}}}) "
                f"MERGE (a)-[r:{_ident(label)} {{id: {cypher_literal(row['id'])}}}]->(b) "
                f"SET r += {cypher_literal(row['props'])};")
    return "\n".join(lines) + "\n"


def _driver(uri, user, password, driver):
    if driver is not None:
        return driver, False
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise ImportError("neo4j is required. Install with: pip install cti-feasibility-metamodel[neo4j]") from exc
    return GraphDatabase.driver(uri, auth=(user, password)), True


def exportToNeo4j(model, uri: str | None = None, user: str | None = None, password: str | None = None, *,
                  database: str | None = None, clear: bool = False, batch_size: int = 500, driver=None) -> dict:
    """Write the model to Neo4j. Returns the number of nodes and relationships written.

    Pass an existing ``driver`` to reuse a connection; otherwise ``uri``, ``user``,
    and ``password`` are used. ``clear`` removes all ``Entity`` nodes first.
    """
    drv, owned = _driver(uri, user, password, driver)
    try:
        with drv.session(database=database) as session:
            for query, params in toCypherStatements(model, batch_size=batch_size, clear=clear):
                session.run(query, params).consume()
    finally:
        if owned:
            drv.close()
    return {"nodes": len(model.entities), "relationships": len(model.relationships)}


NODES_QUERY = f"MATCH (n:{ENTITY_LABEL}) RETURN properties(n) AS props"
EDGES_QUERY = (f"MATCH (a:{ENTITY_LABEL})-[r]->(b:{ENTITY_LABEL}) "
               "RETURN type(r) AS label, properties(r) AS props, a.id AS source, b.id AS target")


def importFromNeo4j(uri: str | None = None, user: str | None = None, password: str | None = None, *,
                    database: str | None = None, strict: bool = True, driver=None):
    """Read all ``Entity`` nodes and the relationships between them into a model."""
    drv, owned = _driver(uri, user, password, driver)
    try:
        with drv.session(database=database) as session:
            nodes = [dict(record["props"]) for record in session.run(NODES_QUERY)]
            edges = [(record["label"], dict(record["props"]), record["source"], record["target"])
                     for record in session.run(EDGES_QUERY)]
    finally:
        if owned:
            drv.close()
    return fromNeo4jRecords(nodes, edges, strict=strict)


def fromNeo4jRecords(nodes: list[dict], edges: list[tuple[str, dict, str, str]], *, strict: bool = True):
    """Build a model from node property maps and (label, properties, source id, target id) edges."""
    entities = [{k: v for k, v in props.items() if k not in DERIVED_NODE_PROPERTIES} for props in nodes]
    relationships = []
    for label, props, source, target in edges:
        item = {k: v for k, v in props.items() if k not in DERIVED_EDGE_PROPERTIES}
        item["type"] = props.get("class") or label
        item["source"] = source
        item["target"] = target
        relationships.append(item)
    return data_to_model({"entities": entities, "relationships": relationships}, strict=strict, coerce=True).model
