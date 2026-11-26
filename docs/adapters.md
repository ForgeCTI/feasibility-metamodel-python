# Adapters

Adapters convert a `Model` to and from external graph libraries and databases. Their dependencies are
optional and imported only when used:

```bash
pip install -e ".[networkx]"   # NetworkX and GraphML
pip install -e ".[neo4j]"      # Neo4j driver
```

## NetworkX

```python
from metamodel.adapters import toNetworkx, fromNetworkx

graph = toNetworkx(model)          # networkx.MultiDiGraph
model = fromNetworkx(graph)
```

* Nodes are entities (key: entity id). Attributes: `type`, `labels` (the type and its superclasses,
  e.g. `["ApplicationInstance", "Code", "Resource"]`), `knowledge_class` (`concept`, `system`,
  `posteriori`), `name`, `description`, `source`, and the domain attributes.
* Edges are relationships (key: relationship id). Attributes: `id`, `type` (class), `label`
  (metamodel label), and relationship attributes; `privilege_level` holds the id of a PrivilegeLevel.
* Scenario metadata is stored in `graph.graph`.
* `toNetworkx(model, flatten=True)` encodes lists and dicts as JSON strings.
* `fromNetworkx` needs a `type` on every node and a `type` or `label` on every edge, so graphs built
  by other tools can be imported too.

```python
resources = [n for n, d in graph.nodes(data=True) if "Resource" in d["labels"]]
grants = [(u, v, d["privilege_level"]) for u, v, d in graph.edges(data=True) if d["label"] == "grantsAccessTo"]
```

## GraphML

```python
from metamodel.adapters import saveGraphML, loadGraphML

saveGraphML(model, "scenario.graphml")
model = loadGraphML("scenario.graphml")
```

## Neo4j

```python
from metamodel.adapters import exportToNeo4j, importFromNeo4j, toCypherStatements, toCypherScript

exportToNeo4j(model, "bolt://localhost:7687", "neo4j", "password", clear=True)
model = importFromNeo4j("bolt://localhost:7687", "neo4j", "password")
statements = toCypherStatements(model)        # [(query, parameters)], batched with UNWIND
script = toCypherScript(model)                 # self-contained script for cypher-shell
```

Graph layout:

* every entity is a node labelled `Entity` and with one label per class in its hierarchy, e.g.
  `(:Entity:ApplicationInstance:Code:Resource)`, so queries can match supertypes; properties are `id`,
  `type`, `knowledge_class`, `name`, `description`, `source`, and the domain attributes (dicts are
  stored as JSON strings); a uniqueness constraint is created on `Entity.id`;
* every relationship has the metamodel label as type (`grantsAccessTo`, `protects`, `instanceOf`, ...)
  and properties `id`, `class` (Python class, used on import), and its attributes; `grantsAccessTo`
  also carries `privilege_level_name` and `privilege_level_rank` for comparisons in queries.

`exportToNeo4j` uses `MERGE` on ids, so exporting the same model twice does not duplicate it; pass
`driver=` to reuse an existing driver and `database=` to choose the database. Example:

```cypher
MATCH (a:Account)-[g:grantsAccessTo]->(r:Resource)<-[:hostsResource]-(m:Node)
      -[:isDestination]->(k:Connection {scope: 'inbound'})
OPTIONAL MATCH (r)-[:requiresPrivilegeLevel]->(req:PrivilegeLevel)
WITH a, g, r, m, req WHERE req IS NULL OR g.privilege_level_rank >= req.rank
RETURN a.name, r.name, m.name
```

See `examples/07_networkx_export` and `examples/08_neo4j_export`.
