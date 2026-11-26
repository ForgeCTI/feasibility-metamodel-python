# CLI

The `metamodel` command is installed with the package (`pip install -e ".[all]"`); without installing,
use `python -m metamodel.cli` with `src` on `PYTHONPATH`.

```text
metamodel validate <input>            validate a scenario
metamodel inspect  <input>            counts by entity and relationship type
metamodel convert  <input> [-o out]   convert between formats
metamodel schema   [name]             entities, relationships, multiplicities
metamodel neo4j export <input>        write a scenario to Neo4j
metamodel neo4j import -o <out>       read a scenario back from Neo4j
```

Common options: `--from {json,yaml,csv,graphml,stix,drawio}` forces the input format (default: from the
extension; a directory is read as CSV), `--lenient` skips unknown types and attributes instead of failing,
and the global `--traceback` shows the full error. Errors are printed as `error: ...` with exit code 2.

## Inputs and outputs

| Format | Input | Output | Notes |
|---|---|---|---|
| `json` | ✓ | ✓ | scenario format (`metadata`, `entities`, `relationships`) |
| `yaml` | ✓ | ✓ | same structure; requires `[yaml]` |
| `csv` | ✓ | ✓ | a directory with `entities.csv`, `relationships.csv`, optional `metadata.json` |
| `graphml` | ✓ | ✓ | through NetworkX; requires `[networkx]` |
| `cypher` | | ✓ | script for `cypher-shell` or Neo4j Browser |
| `stix` | ✓ | | STIX 2.1 bundle (see the STIX parser) |
| `drawio` | ✓ | | simple draw.io scenario diagrams |

Entity and relationship ids are preserved by every format, so conversions can be chained.

## `validate`

```bash
metamodel validate examples/13_motivating_example/data/scenario.yaml
# Valid: True (0 error(s), 0 warning(s))
metamodel validate scenario.json --json      # machine-readable report
metamodel validate scenario.json --strict    # warnings make the command fail
```

Runs reference, type, multiplicity, and semantic checks (connection scopes, acyclic `followedBy`, ranks of
privilege levels). Exit code 1 if the scenario is not valid.

## `inspect`

```bash
metamodel inspect scenario.yaml              # counts by type
metamodel inspect scenario.yaml --entities   # also list ids and names
metamodel inspect scenario.yaml --json
```

## `convert`

```bash
metamodel convert scenario.yaml -o scenario.json
metamodel convert scenario.yaml -o scenario_csv --to csv
metamodel convert scenario_csv -o scenario.graphml
metamodel convert scenario.yaml -o load.cypher
metamodel convert scenario.yaml --to yaml          # print to standard output (json, yaml, cypher)
```

## `schema`

```bash
metamodel schema                 # all entities and relationships
metamodel schema Account         # an entity and every relationship that involves it
metamodel schema grantsAccessTo  # a relationship by label or class name
metamodel schema --json
```

## `neo4j`

```bash
export NEO4J_PASSWORD=password   # also NEO4J_URI, NEO4J_USER, NEO4J_DATABASE
metamodel neo4j export scenario.yaml --clear
metamodel neo4j import -o back.json
```

`--clear` deletes all `Entity` nodes before writing. See [Adapters](adapters.md) for the graph layout.

## In CI

```yaml
- name: Validate scenarios
  run: |
    for f in case_studies/*/scenario.yaml examples/13_motivating_example/data/scenario.yaml; do
      metamodel validate "$f" || exit 1
    done
```
