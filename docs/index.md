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
| `infrastructure` | Models nodes, users, accounts and privilege levels, ports, connections, applications, operating systems, data, code, resources, and security controls. |
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
src/metamodel/cyberThreat/rels/implementsTTP.py
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

* an internal identifier, generated automatically and preserved by the importers;
* identity attributes such as `name` and `description`;
* domain-specific attributes;
* an optional `source` attribute for traceability.

Each entity class also declares its knowledge class (`concept`: a-priori and generic, `system`: a-priori
and instance-specific, `posteriori`: observed or inferred), and generalizations of the metamodel are
Python subclasses (e.g. `Data` and `Asset` are `Resource`s).

### Explicit metamodel relationships

Every relationship is represented as a Python class.

Relationships connect a source entity to a target entity and enforce source/target type compatibility.

Relationship instances have:

* an internal identifier;
* a source entity;
* a target entity;
* cardinality metadata and the metamodel label (e.g. `grantsAccessTo`);
* attributes where the metamodel defines them (e.g. the `PrivilegeLevel` of a grant);
* no traceability attributes.

### Cardinality and consistency validation

The package includes validators for checking that instantiated scenarios respect the metamodel.

Validation includes:

* relationship source and target type checks;
* missing reference checks;
* cardinality checks, following the multiplicities of the paper;
* semantic checks (connection scopes, acyclic threat-step ordering, privilege-level ranks);
* whole-model validation reports.

### Taxonomy integration

The package supports controlled vocabularies and reusable taxonomies.

Taxonomies can be used for concepts such as:

* attack tools;
* TTPs;
* vulnerabilities;
* node types;
* user types;
* data types;
* sectors;
* countries;
* security requirements;
* platforms.

Taxonomy concepts are looked up with `TaxonomyRegistry` (e.g. `attackTools:cobaltStrike`) and used to
instantiate entities; identifiers from external catalogues are kept in attributes such as
`TTP.external_id`. This keeps reusable reference knowledge separate from scenario-specific instances.

### I/O support

The `io` module loads and saves scenarios in JSON, YAML, and CSV, and imports STIX 2.1 bundles and
draw.io diagrams. Identifiers, relationship attributes, and scenario metadata are preserved.

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

The package includes adapters, in both directions, for NetworkX, GraphML, and Neo4j (driver or
Cypher script).

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

organization = model.add(
    Organization(
        name="ExampleBank",
        description="Example financial organization",
        source="Example scenario"
    )
)

sector = model.add(Sector(name="Finance"))

model.add(
    operatesIn(
        source_entity=organization,
        target_entity=sector
    )
)

report = model.validate()

print(report.is_valid)   # False: the organization lacks, e.g., a home country and an infrastructure
for error in report.errors:
    print(error.message)
```

## Typical workflow

A common usage workflow is:

```text
1. Define or load a scenario.
2. Instantiate entities and relationships.
3. Validate relationship types, references, and cardinalities.
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
| [Schema reference](schema.md)   | Every entity, attribute, relationship, and multiplicity (generated).           |
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

Version 0.2.0 aligns the entities, relationships, and multiplicities with the paper (43 entities,
65 relationship classes). The evaluation of threat-step preconditions (graph patterns and their
Cypher translation) is under development; see the [changelog](https://github.com/ForgeCTI/feasibility-metamodel-python/blob/main/CHANGELOG.md).
