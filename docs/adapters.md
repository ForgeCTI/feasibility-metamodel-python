# Adapters

Adapters convert a CTI Feasibility Metamodel `Model` into representations used by external libraries, graph databases, and analysis tools.

The package keeps adapters separate from the core metamodel so that the core remains lightweight and independent from optional third-party dependencies.

## Purpose

The **CTI Feasibility Metamodel** represents scenarios as Python objects:

```text
Entity objects + Relationship objects → Model
```

Adapters translate this internal model into external representations.

Typical use cases include:

* graph analysis with NetworkX;
* graph storage and querying with Neo4j;
* graph exchange through GraphML;
* visualization with external graph tools;
* future integration with RDF, OWL, STIX, pandas, or other ecosystems.

## Adapters versus I/O

The package distinguishes between `io` and `adapters`.

| Component  | Responsibility                                            | Examples                        |
| ---------- | --------------------------------------------------------- | ------------------------------- |
| `io`       | Reads and writes scenario files or CTI input formats.     | JSON, YAML, CSV, draw.io, STIX. |
| `adapters` | Converts models to external libraries or runtime systems. | NetworkX, Neo4j, GraphML.       |

In short:

```text
io/
  scenario files and parsers

adapters/
  external graph libraries, databases, and analysis ecosystems
```

For example:

```text
scenario.yaml → io → Model → adapters → NetworkX graph
bundle.json   → io → Model → adapters → Neo4j database
Model         → adapters → GraphML file
```

## Module location

Adapters are located under:

```text
src/metamodel/adapters/
```

Recommended structure:

```text
src/metamodel/adapters/
├── __init__.py
├── networkxAdapter.py
├── neo4jAdapter.py
└── graphmlAdapter.py
```

Future adapters may include:

```text
rdfAdapter.py
owlAdapter.py
pandasAdapter.py
stixAdapter.py
cytoscapeAdapter.py
```

## Optional dependencies

Adapters usually require optional dependencies.

Install only the dependencies you need.

### NetworkX

```bash
pip install -e ".[networkx]"
```

or from PyPI:

```bash
pip install "cti-feasibility-metamodel[networkx]"
```

### Neo4j

```bash
pip install -e ".[neo4j]"
```

or from PyPI:

```bash
pip install "cti-feasibility-metamodel[neo4j]"
```

### Full installation

```bash
pip install -e ".[all]"
```

## Validation before adaptation

Always validate a model before converting it through an adapter.

```python
report = model.validate()

if not report.is_valid:
    raise RuntimeError("Cannot export an invalid model.")

# Safe to export after this point.
```

This avoids exporting broken references, invalid relationship endpoints, or incomplete scenarios.

Recommended workflow:

```text
Model
  ↓
validate
  ↓
adapt/export
  ↓
external analysis system
```

## Graph representation

Most adapters represent the metamodel as a directed graph.

Entities become graph nodes.

Relationships become graph edges.

```text
Entity       → node
Relationship → directed edge
```

Example:

```text
Organization("ExampleBank") --operatesIn--> Sector("Finance")
```

becomes:

```text
Node: Organization / ExampleBank
Node: Sector / Finance
Edge: operatesIn
```

## Node attributes

When converting entities to graph nodes, adapters should preserve useful attributes.

Recommended node attributes:

| Attribute         | Meaning                                                                          |
| ----------------- | -------------------------------------------------------------------------------- |
| `id`              | Internal generated entity identifier.                                            |
| `type`            | Entity type, derived from the class name.                                        |
| `name`            | Human-readable name.                                                             |
| `description`     | Optional description.                                                            |
| `source`          | Optional traceability source.                                                    |
| `taxonomy_ref`    | Optional taxonomy reference, where available.                                    |
| domain attributes | Entity-specific attributes such as `cvss_score`, `ip_addresses`, or `tool_type`. |

Example node payload:

```json
{
  "id": "generated-id",
  "type": "AttackTool",
  "name": "Cobalt Strike",
  "taxonomy_ref": "attackTools:cobaltStrike",
  "tool_type": "command_and_control"
}
```

## Edge attributes

Relationships become directed edges.

Recommended edge attributes:

| Attribute | Meaning                                         |
| --------- | ----------------------------------------------- |
| `id`      | Internal generated relationship identifier.     |
| `type`    | Relationship type, derived from the class name. |
| `source`  | Internal ID of the source entity.               |
| `target`  | Internal ID of the target entity.               |

For generic STIX relationships, additional attributes may be available:

| Attribute                | Meaning                               |
| ------------------------ | ------------------------------------- |
| `stix_relationship_type` | Original STIX relationship type.      |
| `stix_id`                | Original STIX relationship object ID. |

Example edge payload:

```json
{
  "id": "generated-relationship-id",
  "type": "targetsResource",
  "source": "threat-step-id",
  "target": "resource-id"
}
```

## NetworkX adapter

The NetworkX adapter converts a model into a `networkx.MultiDiGraph`.

A multidigraph is recommended because the metamodel may contain multiple relationships between the same pair of entities.

Example:

```python
from metamodel.adapters.networkxAdapter import toNetworkx

graph = toNetworkx(model)
```

Then inspect the graph:

```python
print(graph.number_of_nodes())
print(graph.number_of_edges())
```

### Example: basic graph traversal

```python
from metamodel.adapters.networkxAdapter import toNetworkx

graph = toNetworkx(model)

for node_id, data in graph.nodes(data=True):
    print(node_id, data["type"], data["name"])

for source, target, key, data in graph.edges(keys=True, data=True):
    print(source, target, data["type"])
```

### Example: find outgoing relationships

```python
entity_id = some_entity.id

for _, target, data in graph.out_edges(entity_id, data=True):
    print(data["type"], target)
```

### Example: filter by entity type

```python
threat_steps = [
    node_id
    for node_id, data in graph.nodes(data=True)
    if data.get("type") == "ThreatStep"
]

print(threat_steps)
```

### Example: find targeted resources

```python
targeted_resources = []

for source, target, data in graph.edges(data=True):
    if data.get("type") == "targetsResource":
        targeted_resources.append(target)

print(targeted_resources)
```

## Neo4j adapter

The Neo4j adapter exports a model to a Neo4j graph database.

Neo4j is useful when scenarios become large, when graph queries are needed, or when multiple case studies need to be stored and queried together.

Example:

```python
from metamodel.adapters.neo4jAdapter import exportToNeo4j

exportToNeo4j(
    model=model,
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
)
```

### Recommended Neo4j representation

Entities should be exported as nodes.

Each node should have:

```text
:Entity
:<EntityType>
```

For example:

```text
(:Entity:Organization)
(:Entity:ThreatStep)
(:Entity:AttackTool)
(:Entity:Resource)
```

Relationships should be exported as directed relationships.

The relationship type can be upper snake case:

```text
operatesIn      → OPERATES_IN
targetsResource → TARGETS_RESOURCE
implementsTtp   → IMPLEMENTS_TTP
```

Example graph pattern:

```cypher
(:ThreatStep)-[:TARGETS_RESOURCE]->(:Resource)
```

### Example Cypher queries

Find all threat steps that target resources:

```cypher
MATCH (step:ThreatStep)-[:TARGETS_RESOURCE]->(resource:Resource)
RETURN step.name, resource.name
```

Find all vulnerabilities exploited by threat steps:

```cypher
MATCH (step:ThreatStep)-[:EXPLOITS]->(vulnerability:Vulnerability)
RETURN step.name, vulnerability.name, vulnerability.severity, vulnerability.cvss_score
```

Find all assets exposed through targeted resources:

```cypher
MATCH (step:ThreatStep)-[:TARGETS_RESOURCE]->(resource:Resource)-[:IMPLEMENTS_ASSET]->(asset:Asset)
RETURN step.name, resource.name, asset.name
```

Find all TTPs implemented by a threat:

```cypher
MATCH (threat:Threat)-[:STARTS_WITH|FOLLOWED_BY*]->(step:ThreatStep)-[:IMPLEMENTS_TTP]->(ttp:TTP)
RETURN threat.name, step.name, ttp.name, ttp.external_id
```

## Running Neo4j locally

For local testing, use Docker.

Example `docker-compose.yml`:

```yaml
services:
  neo4j:
    image: neo4j:5
    container_name: cti-feasibility-neo4j
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/password
```

Start Neo4j:

```bash
docker compose up -d
```

Open the Neo4j browser:

```text
http://localhost:7474
```

Credentials:

```text
username: neo4j
password: password
```

Then export a model:

```python
from metamodel.adapters.neo4jAdapter import exportToNeo4j

exportToNeo4j(
    model,
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
)
```

## GraphML adapter

GraphML is useful for exchange with graph tools such as Gephi, yEd, Cytoscape, or other visualization software.

Example:

```python
from metamodel.adapters.graphmlAdapter import saveGraphML

saveGraphML(model, "scenario.graphml")
```

A common implementation strategy is:

```text
Model → NetworkX MultiDiGraph → GraphML file
```

If using NetworkX internally:

```python
import networkx as nx

from metamodel.adapters.networkxAdapter import toNetworkx

graph = toNetworkx(model)
nx.write_graphml(graph, "scenario.graphml")
```

## Adapter design principles

Adapters should follow these rules.

| Principle                    | Meaning                                                      |
| ---------------------------- | ------------------------------------------------------------ |
| Do not mutate the model      | Adapters should not modify entities or relationships.        |
| Preserve identifiers         | Internal IDs should be included in exported nodes and edges. |
| Preserve types               | Entity and relationship type names should be exported.       |
| Preserve attributes          | Domain attributes should be included where possible.         |
| Preserve taxonomy references | `taxonomy_ref` should be exported when present.              |
| Validate first               | Export should fail or warn when the model is invalid.        |
| Keep dependencies optional   | Adapter dependencies should be installed only when needed.   |

## Attribute serialization

Adapters should convert Python attributes into external-system-friendly values.

Examples:

| Python value             | Export representation                                               |
| ------------------------ | ------------------------------------------------------------------- |
| `None`                   | omitted or `null`, depending on target system.                      |
| `list[str]`              | list property, JSON string, or repeated values depending on target. |
| `dict`                   | JSON string if the target does not support dictionaries.            |
| `bool`                   | boolean property.                                                   |
| `int` / `float`          | numeric property.                                                   |
| `datetime` / date string | ISO-formatted string.                                               |

Neo4j supports several property types, but nested dictionaries are often better converted into JSON strings.

GraphML has more limited support, so complex values may need to be converted to strings.

## STIX and adapters

The STIX parser can produce:

* native metamodel entities;
* `GenericStixObject`;
* `GenericStixRelationship`.

Adapters should preserve these objects.

For example, a generic STIX object node should include:

```json
{
  "type": "GenericStixObject",
  "stix_type": "course-of-action",
  "stix_id": "course-of-action--...",
  "name": "Example course of action"
}
```

A generic STIX relationship edge should include:

```json
{
  "type": "GenericStixRelationship",
  "stix_relationship_type": "uses",
  "stix_id": "relationship--..."
}
```

This ensures that imported CTI is not lost when exported to a graph representation.

## Recommended export workflow

For a case study:

```text
case study implementation
        ↓
build Model
        ↓
validate Model
        ↓
export to NetworkX or Neo4j
        ↓
run graph analysis
        ↓
save results under output/
```

Suggested folder structure:

```text
case_studies/01_case_study/
├── implementation.py
├── scenario.yaml
├── output/
│   ├── validation_report.json
│   ├── graph.graphml
│   └── neo4j_export.log
└── notes/
    └── assumptions.md
```

## Example: end-to-end export

```python
from metamodel.adapters.networkxAdapter import toNetworkx

model = build_model()

report = model.validate()

if not report.is_valid:
    raise RuntimeError(report.errors)

graph = toNetworkx(model)

print("Nodes:", graph.number_of_nodes())
print("Edges:", graph.number_of_edges())
```

## Example: exporting a STIX-derived model

```python
from metamodel.io.stixParser import loadStixBundleWithReport
from metamodel.adapters.networkxAdapter import toNetworkx

result = loadStixBundleWithReport("bundle.json")

model = result.model
report = model.validate()

if not report.is_valid:
    raise RuntimeError(report.errors)

graph = toNetworkx(model)

print("STIX objects skipped:", len(result.skipped_objects))
print("STIX relationships skipped:", len(result.skipped_relationships))
print("Graph nodes:", graph.number_of_nodes())
print("Graph edges:", graph.number_of_edges())
```

## Common issues

### NetworkX is not installed

Problem:

```text
ModuleNotFoundError: No module named 'networkx'
```

Fix:

```bash
pip install -e ".[networkx]"
```

or:

```bash
pip install "cti-feasibility-metamodel[networkx]"
```

### Neo4j connection fails

Check that Neo4j is running:

```bash
docker compose ps
```

Check the URI:

```text
bolt://localhost:7687
```

Check the credentials:

```text
neo4j / password
```

Check that the Neo4j Python driver is installed:

```bash
pip install -e ".[neo4j]"
```

### GraphML export fails

GraphML does not support all Python object types directly.

Convert complex attributes such as lists or dictionaries to strings before writing the file.

### Exported graph is empty

Check that:

* entities were added to the model;
* relationships were added to the model;
* the adapter receives the correct `Model` object;
* validation passes before export.

## Practical checklist

Before using an adapter:

* Is the required optional dependency installed?
* Does the model contain the expected entities?
* Does the model contain the expected relationships?
* Does `model.validate()` return `is_valid = True`?
* Are taxonomy references preserved?
* Are STIX generic objects preserved?
* Are generated outputs written under `output/`?
* Are credentials or secrets excluded from version control?

## Next steps

Continue with:

* [I/O](io.md) to understand how models are loaded from files and CTI sources;
* [Validation](validation.md) to validate models before export;
* [Taxonomies](taxonomies.md) to understand taxonomy references in exported graphs;
* [Quickstart](quickstart.md) for a complete executable scenario.
