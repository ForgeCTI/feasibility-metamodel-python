# CTI Feasibility Metamodel

**CTI Feasibility Metamodel** is a Python package for modelling scenarios where **organizational context**, **infrastructure state**, and **cyber-threat intelligence** interact.

The package supports feasibility analysis, scenario modelling, graph conversion, and structured validation of cyber-threat scenarios. It provides a metamodel-oriented object model where entities and relationships are explicit, typed, validated, and reusable.

## Purpose

Cyber attacks cannot be evaluated only from a technical perspective. Their feasibility depends on how threat capabilities interact with the target organization, its infrastructure, its assets, its users, and its security requirements.

The **CTI Feasibility Metamodel** provides a structured way to represent those dependencies.

It helps answer questions such as:

* Which organizational assets are exposed to a given threat?
* Which attack steps are feasible in a specific infrastructure?
* Which vulnerabilities, users, applications, or nodes enable an attack path?
* Which security requirements are compromised by a threat step?
* How can a scenario be converted into a graph for analysis in NetworkX or Neo4j?

## Metamodel structure

The package is organized around three interconnected sub-metamodels.

| Sub-metamodel    | Purpose                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `organization`   | Models organizational context, sectors, countries, assets, business requirements, and security requirements.              |
| `infrastructure` | Models nodes, users, ports, connections, applications, operating systems, information, code, and resources.               |
| `cyberThreat`    | Models threat actors, adversaries, campaigns, threats, threat steps, TTPs, vulnerabilities, indicators, and attack tools. |

Each sub-metamodel is organized into:

```text
entities/
rels/
```

Each entity has its own file.
Each relationship has its own file.

For example:

```text
src/metamodel/cyberThreat/entities/AttackTool.py
src/metamodel/cyberThreat/entities/TTP.py
src/metamodel/cyberThreat/rels/exploits.py
src/metamodel/cyberThreat/rels/implementsTtp.py
```

## Main features

### Explicit metamodel entities

Every entity is represented as a standard Python class.

Entity file names and class names match the exact entity name in the metamodel.

```text
AttackTool.py  →  class AttackTool
TTP.py         →  class TTP
OS.py          →  class OS
```

Entity instances have:

* an internal automatically generated identifier;
* identity attributes such as `name` and `description`;
* domain-specific attributes;
* an optional `source` attribute for traceability.

### Explicit metamodel relationships

Every relationship is represented as a Python class.

Relationships connect a source entity to a target entity and enforce source/target type compatibility.

Relationship instances have:

* an internal automatically generated identifier;
* a source entity;
* a target entity;
* cardinality metadata;
* no traceability attributes.

### Cardinality and consistency validation

The package includes validators for checking that instantiated scenarios respect the metamodel.

Validation includes:

* relationship source and target type checks;
* missing reference checks;
* cardinality checks;
* taxonomy reference checks;
* whole-model validation reports.

### Taxonomy integration

The package supports controlled vocabularies and reusable taxonomies.

Taxonomies can be used for concepts such as:

* attack tools;
* TTPs;
* vulnerabilities;
* node types;
* user types;
* information types;
* sectors;
* countries;
* security requirements;
* platforms.

For example, a scenario-specific `AttackTool` can reference a taxonomy concept:

```yaml
type: AttackTool
name: Cobalt Strike
taxonomy_ref: attackTools:cobaltStrike
```

This keeps reusable reference knowledge separate from scenario-specific instances.

### I/O support

The `io` module supports loading and saving metamodel scenarios.

Supported or planned formats include:

* JSON;
* YAML;
* CSV;
* draw.io diagrams.

The typical flow is:

```text
scenario file
    ↓
parser
    ↓
Model object
    ↓
validation
    ↓
validated scenario
```

### Graph adapters

The package includes adapters for converting metamodel scenarios into graph-based representations.

Supported or planned adapters include:

* NetworkX;
* Neo4j;
* GraphML.

This makes it possible to analyze scenarios as graphs, compute paths, inspect neighborhoods, or store the model in a graph database.

## Installation

Install the base package with:

```bash
pip install cti-feasibility-metamodel
```

Install optional dependencies only when needed:

```bash
pip install cti-feasibility-metamodel[yaml]
pip install cti-feasibility-metamodel[networkx]
pip install cti-feasibility-metamodel[neo4j]
```

For development:

```bash
pip install -e ".[all]"
```

## Minimal example

```python
from metamodel.core.Model import Model

from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn

model = Model()

organization = model.add_entity(
    Organization(
        name="ExampleBank",
        description="Example financial organization",
        source="Example scenario"
    )
)

sector = model.add_entity(
    Sector(
        name="Finance",
        taxonomy_ref="sectors:finance"
    )
)

model.add_relationship(
    operatesIn(
        source_entity=organization,
        target_entity=sector
    )
)

report = model.validate()

print(report.is_valid)
print(report.errors)
```

## Typical workflow

A common usage workflow is:

```text
1. Define or load a scenario.
2. Instantiate entities and relationships.
3. Validate relationship types, references, cardinalities, and taxonomy references.
4. Export the scenario to another representation, such as NetworkX or Neo4j.
5. Use the resulting model for feasibility analysis or graph-based reasoning.
```

## Documentation map

Start with the following pages:

| Page                            | Description                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------ |
| [Installation](installation.md) | How to install the package and optional dependencies.                          |
| [Quickstart](quickstart.md)     | A minimal end-to-end modelling example.                                        |
| [Metamodel](metamodel.md)       | Overview of the organization, infrastructure, and cyber-threat sub-metamodels. |
| [Taxonomies](taxonomies.md)     | How controlled vocabularies are represented and referenced.                    |
| [Validation](validation.md)     | How model correctness is checked.                                              |
| [I/O](io.md)                    | How scenarios are loaded from and saved to files.                              |
| [Adapters](adapters.md)         | How models are converted to NetworkX, Neo4j, or other graph representations.   |
| [CLI](cli.md)                   | How to use the package from the command line.                                  |

## Design principles

The package follows a few core design principles.

| Principle                     | Meaning                                                                 |
| ----------------------------- | ----------------------------------------------------------------------- |
| Explicit structure            | Entities and relationships are first-class Python objects.              |
| One file per concept          | Each entity and relationship is defined in its own file.                |
| Type safety                   | Relationships check that they connect compatible entity types.          |
| Cardinality awareness         | Relationship multiplicities are represented and validated.              |
| Taxonomy separation           | Reusable controlled vocabularies are separated from scenario instances. |
| Interoperability              | Models can be converted to graph libraries and external systems.        |
| Documentation-first modelling | The code structure mirrors the conceptual metamodel.                    |

## Project status

The **CTI Feasibility Metamodel** is currently an early implementation of a metamodel-oriented Python framework for CTI-driven feasibility analysis.

The current focus is on:

* stabilizing the entity and relationship structure;
* improving attribute validation;
* expanding taxonomy coverage;
* improving scenario parsers;
* strengthening cardinality validation;
* extending graph export capabilities;
* improving documentation and examples.
