# Neo4j export

## Purpose

Load the motivating example of the paper into Neo4j, read it back, and query it.

## Run

```bash
pip install -e ".[yaml,neo4j]"
docker compose -f examples/08_neo4j_export/docker-compose.yml up -d
NEO4J_PASSWORD=password python examples/08_neo4j_export/main.py
```

Or, with the CLI:

```bash
metamodel neo4j export examples/13_motivating_example/data/scenario.yaml --password password --clear
metamodel neo4j import -o back.json --password password
metamodel convert examples/13_motivating_example/data/scenario.yaml -o load.cypher   # offline script
```

## Graph layout

* nodes: label `Entity` plus one label per class in the hierarchy
  (e.g. `:Entity:ApplicationInstance:Code:Resource`), properties `id`, `type`,
  `knowledge_class`, `name`, and the domain attributes;
* relationships: the metamodel label as type (e.g. `grantsAccessTo`), properties `id`,
  `class` (Python class), and attributes; `grantsAccessTo` also carries
  `privilege_level_name` and `privilege_level_rank` for comparisons.

`queries/ts3_precondition.cypher` illustrates how a precondition of the paper reads in Cypher.
