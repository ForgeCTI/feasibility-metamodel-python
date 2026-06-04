# Examples

This folder contains executable examples for the CTI Feasibility Metamodel.

Each example is self-contained in its own sub-folder. This makes it possible to keep code, input files, generated outputs, Cypher queries, diagrams, and auxiliary material organized together.

## Structure

| Example | Purpose |
|---|---|
| `01_organization_scenario` | Instantiate organization entities and relationships. |
| `02_infrastructure_scenario` | Instantiate infrastructure entities and relationships. |
| `03_cyber_threat_scenario` | Instantiate cyber-threat entities and relationships. |
| `04_full_scenario` | Build an integrated organization-infrastructure-threat scenario. |
| `05_cardinality_validation` | Demonstrate validation errors and validation reports. |
| `06_taxonomy_usage` | Use taxonomy references for reusable concepts. |
| `07_networkx_export` | Convert a model to a NetworkX graph. |
| `08_neo4j_export` | Export a model to Neo4j and inspect it with Cypher. |
| `09_yaml_scenario_import` | Load a scenario from YAML. |
| `10_json_scenario_import` | Load a scenario from JSON. |
| `11_drawio_instantiation` | Instantiate a model from a draw.io file. |
| `12_stix_parser` | Parse STIX CTI data into metamodel entities. |

## How to run

From the repository root, install the package in editable mode:

```bash
pip install -e ".[all]"
```

Then run any example:

```bash
python examples/01_organization_scenario/main.py
```

Examples use paths relative to their own folder, so they can also be run from other working directories.
