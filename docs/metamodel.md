# Metamodel

The **CTI Feasibility Metamodel** provides a structured representation of scenarios where **cyber-threat intelligence**, **organizational context**, and **infrastructure state** interact.

The metamodel is designed to support feasibility analysis. In this context, feasibility means assessing whether a threat, attack step, TTP, vulnerability, or attack tool can realistically affect a specific organization and infrastructure.

## Overview

The metamodel is organized into three interconnected sub-metamodels:

| Sub-metamodel    | Purpose                                                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `organization`   | Represents the organizational context in which feasibility is assessed.                                                 |
| `infrastructure` | Represents the technical environment, resources, users, and information assets.                                         |
| `cyberThreat`    | Represents CTI concepts such as threat actors, threats, campaigns, TTPs, vulnerabilities, indicators, and attack tools. |

These sub-metamodels are connected through relationships. For example, a threat step can target an infrastructure resource, exploit a vulnerability, and compromise a security requirement associated with an organizational asset.

## Package organization

The Python package mirrors the metamodel structure.

```text
src/metamodel/
├── organization/
│   ├── entities/
│   └── rels/
│
├── infrastructure/
│   ├── entities/
│   └── rels/
│
└── cyberThreat/
    ├── entities/
    └── rels/
```

Each entity has its own file.

```text
src/metamodel/cyberThreat/entities/AttackTool.py
src/metamodel/cyberThreat/entities/TTP.py
src/metamodel/infrastructure/entities/Node.py
src/metamodel/organization/entities/Organization.py
```

Each relationship also has its own file.

```text
src/metamodel/cyberThreat/rels/exploits.py
src/metamodel/cyberThreat/rels/implementsTTP.py
src/metamodel/infrastructure/rels/exposesPort.py
src/metamodel/organization/rels/operatesIn.py
```

## Naming conventions

The package follows strict naming conventions.

| Concept            | Convention                  | Example                        |
| ------------------ | --------------------------- | ------------------------------ |
| Entity file        | Exact metamodel entity name | `AttackTool.py`                |
| Entity class       | Exact metamodel entity name | `class AttackTool`             |
| Relationship file  | Short lower camel case      | `targetsResource.py`           |
| Relationship class | Short lower camel case      | `class targetsResource`        |
| Python attributes  | Snake case                  | `ip_addresses`, `privilege_level` |

Entity names preserve acronyms when they are part of the metamodel.

```text
TTP.py  →  class TTP
OS.py   →  class OS
```

## Entity model

Entities are standard Python classes.

Each entity instance has:

* an internal automatically generated identifier;
* a `type` derived from the Python class name;
* identity attributes;
* domain-specific attributes;
* an optional `source` attribute;
* a class-level `knowledge_class`: `concept` (a-priori, generic), `system` (a-priori,
  instance-specific), or `posteriori` (observed or inferred), as in the paper.

The internal identifier is generated automatically; importers restore the identifiers stored in files.
Generalizations of the metamodel are Python subclasses: `Code`, `Data`, and `Asset` are `Resource`s,
`ApplicationInstance` and `OSInstance` are `Code`, and the three vulnerability kinds are `Vulnerability`s.

```python
from metamodel.organization.entities.Organization import Organization

organization = Organization(name="ExampleBank")

print(organization.id)
print(organization.type)
print(organization.name)
```

The `type` is derived from the class name.

```text
Organization
AttackTool
TTP
Node
```

Entities do not store relationship lists as attributes. Connections between entities are represented only by relationship objects.

## Relationship model

Relationships are also standard Python classes.

Each relationship instance has:

* an internal automatically generated identifier;
* a source entity;
* a target entity;
* source and target type constraints;
* cardinality metadata;
* the metamodel label and, for some relationships, attributes.

Relationships do not include a traceability `source` attribute. Traceability is stored at the entity level when needed.

Each relationship class also declares its metamodel `label` (e.g. `grantsAccessTo`), which importers accept in
place of the class name (e.g. `grantsAccessToNode`) and which the Neo4j adapter uses as relationship type.
A relationship may carry attributes: `grantsAccessTo` has `privilege_level`, an entity-valued attribute
(the association class `PrivilegeLevel` of the paper), which must belong to the same model.

Example:

```python
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn

organization = Organization(name="ExampleBank")
sector = Sector(name="Finance")

relationship = operatesIn(
    source_entity=organization,
    target_entity=sector,
)
```

The relationship connects:

```text
Organization → Sector
```

If a relationship is instantiated with an incompatible source or target entity, the package raises an error.

## Cardinalities

Relationships include cardinality metadata.

Cardinality validation checks whether the instantiated model respects the multiplicities defined by the metamodel.

Examples of cardinality constraints include:

```text
1
0..1
1..*
0..*
```

Cardinality validation is performed at the model level because it requires knowledge of all entities and relationships in a scenario.

<!-- no-test -->
```python
report = model.validate()

if not report.is_valid:
    for error in report.errors:
        print(error)
```

## Organization sub-metamodel

The organization sub-metamodel represents the organizational context in which feasibility is assessed.

It captures the organization, its sector, jurisdictional context, business requirements, security requirements, and assets.

The entities, attributes, relationships, and multiplicities of the Organization sub-metamodel are listed in the [schema reference](schema.md#organization), generated from the code.

The organization sub-metamodel is important because feasibility is not only technical. A threat may be technically possible but more or less relevant depending on the organization’s sector, assets, requirements, and exposure.

## Infrastructure sub-metamodel

The infrastructure sub-metamodel represents the technical environment in which threat feasibility is evaluated.

It captures nodes, users, ports, connections, applications, operating systems, code, information, and resources.

The entities, attributes, relationships, and multiplicities of the Infrastructure sub-metamodel are listed in the [schema reference](schema.md#infrastructure), generated from the code.

Notable elements (aligned with the paper):

* `Code`, `Data`, and `Asset` specialize `Resource`; `ApplicationInstance` and `OSInstance` specialize `Code`.
* `Connection.scope` is `internal`, `inbound` (destination only), or `outbound` (source only).
* A `User` has `Account`s (`kind`: local, domain, cloud, service); `grantsAccessTo` links an account to a node or
  resource and carries the association class `PrivilegeLevel` as the attribute `privilege_level`; a resource may
  require a minimum level (`requiresPrivilegeLevel`). Privilege levels are ordered by `rank`.
* A deployed `SecurityControl` is an instance of a generic `SecurityControlType`; it `protects` nodes, users,
  accounts, and resources and `mitigates` vulnerabilities, while the type `counters` TTPs.
* `ApplicationInstance --uses--> Port` replaces `listensOn`; `Data`/`DataType` replace `Information`/`InformationType`.

The infrastructure sub-metamodel is the main bridge between abstract CTI and concrete feasibility. It represents whether the technical conditions required by a threat step are present in the scenario.

## Cyber-threat sub-metamodel

The cyber-threat sub-metamodel represents CTI concepts relevant to feasibility analysis.

It captures adversaries, threat actors, campaigns, threats, attack steps, TTPs, vulnerabilities, indicators, attack tools, and configurations.

The entities, attributes, relationships, and multiplicities of the Cyber threat sub-metamodel are listed in the [schema reference](schema.md#cyber-threat), generated from the code.

`ThreatStep.join` (`AND` by default, or `OR`) states how the outcomes of several predecessors are combined;
`followedBy` must be acyclic. A `ConfigVulnerability` may affect code or accounts.

The cyber-threat sub-metamodel captures CTI knowledge in a form that can be checked against a concrete organization and infrastructure.

## Cross-sub-metamodel relationships

The metamodel is useful because the three sub-metamodels are connected.

Examples:

```text
Organization → Infrastructure
ThreatStep → Resource
SecurityControlType → TTP
ThreatStep → Vulnerability
ThreatStep → AssetSecurityRequirement
Campaign → Sector
Campaign → HomeCountry
TTP → SecurityRequirement
SoftwareVulnerability → Application
SoftwareVulnerability → OS
HumanVulnerability → User
```

These cross-sub-metamodel relationships make it possible to reason about feasibility.

For example:

```text
ThreatStep
    exploits Vulnerability
    targets Resource
    implements TTP

Asset (a Resource)
    hosted on Node
    accessible through Account (grantsAccessTo, with a PrivilegeLevel)

Node
    exposes Port
    runs OSInstance
    runs ApplicationInstance

Asset
    has AssetSecurityRequirement
```

This allows a threat step to be evaluated against actual infrastructure conditions and organizational requirements.

## Taxonomies

Reusable controlled vocabularies (attack tools, ATT&CK techniques, sectors, node types, data types,
...) are kept in taxonomies, separate from scenario instances:

```text
Taxonomy concept:  generic reusable knowledge, e.g. attackTools:cobaltStrike
Scenario instance: concrete object in a specific model, e.g. AttackTool(name="Cobalt Strike")
```

Entities are instantiated from taxonomy concepts, and external identifiers are kept in attributes such
as `TTP.external_id`:

```python
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.taxonomies.TaxonomyRegistry import TaxonomyRegistry

taxonomies = TaxonomyRegistry.load_default()
concept = taxonomies.resolve("mitreAttackEnterprise:T1059")
ttp = TTP(name=concept.name, external_id=concept.id)
```

See [Taxonomies](taxonomies.md).

## STIX integration

The package includes an extensible STIX parser under the `io` module.

STIX objects can be mapped to native metamodel entities where a clear semantic correspondence exists.

Examples:

| STIX object type | Native metamodel entity |
| ---------------- | ----------------------- |
| `attack-pattern` | `TTP`                   |
| `campaign`       | `Campaign`              |
| `indicator`      | `Indicator`             |
| `intrusion-set`  | `Adversary`             |
| `malware`        | `AttackTool`            |
| `threat-actor`   | `ThreatActor`           |
| `tool`           | `AttackTool`            |
| `vulnerability`  | `Vulnerability`         |

Other STIX objects can be preserved as generic STIX entities, so information is not lost.

STIX relationship objects can be preserved as generic STIX relationships. This makes the STIX integration extensible while avoiding incorrect semantic assumptions.

## Model container

A complete scenario is represented by a `Model`.

The model stores entities and relationships.

<!-- no-test -->
```python
from metamodel.core.Model import Model

model = Model()

model.add(entity)
model.add(relationship)
```

The model is responsible for whole-scenario operations such as validation and export.

<!-- no-test -->
```python
report = model.validate()
```

## Validation

The metamodel supports several validation levels.

| Validation type        | Purpose                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| Type validation        | Checks that relationships connect compatible entity types.          |
| Reference validation   | Checks that relationships point to existing entities.               |
| Cardinality validation | Checks relationship multiplicities.                                 |
| Semantic validation    | Checks connection scopes, acyclic `followedBy`, privilege-level ranks. |
| Model validation       | Runs all relevant checks on a complete scenario.                    |

Validation returns a report.

<!-- no-test -->
```python
report = model.validate()

print(report.is_valid)
print(report.errors)
```

## Example structure

A simple scenario may contain:

```text
Organization: ExampleBank
Sector: Finance
Infrastructure: Production infrastructure
Node: public-web-01
Data: Customer records
User: Portal administrator, with Account admin@portal (PrivilegeLevel: Administrator)
ThreatActor: Example actor
Threat: Web portal compromise
ThreatStep: Exploit public-facing web application
TTP: Exploit Public-Facing Application
Vulnerability: CVE-like vulnerability
```

with relationships such as:

```text
ExampleBank operatesIn Finance
ExampleBank manages Production infrastructure
Production infrastructure madeBy public-web-01
public-web-01 hostsResource Customer records
admin@portal grantsAccessTo Customer records (privilege_level: Administrator)
Example actor initiates Web portal compromise
Web portal compromise startsWith Exploit public-facing web application
Exploit public-facing web application implements Exploit Public-Facing Application
Exploit public-facing web application exploits CVE-like vulnerability
Exploit public-facing web application targetsResource Customer records
```

## Design principles

The metamodel follows these principles:

| Principle                   | Description                                                                 |
| --------------------------- | --------------------------------------------------------------------------- |
| Explicit concepts           | Entities and relationships are first-class objects.                         |
| One file per concept        | Each entity and relationship is defined in its own file.                    |
| Typed relationships         | Relationship classes enforce source and target compatibility.               |
| Cardinality-aware modelling | Relationship multiplicities are represented and validated.                  |
| Taxonomy separation         | Reusable taxonomies are kept separate from scenario instances.              |
| Extensibility               | Parsers, taxonomies, and adapters can be extended.                          |
| Graph compatibility         | Models can be converted to graph representations such as NetworkX or Neo4j. |
| Documentation alignment     | The package structure mirrors the conceptual metamodel.                     |

## Next steps

Continue with:

* [Taxonomies](taxonomies.md) to understand controlled vocabulary integration;
* [Validation](validation.md) to understand model correctness checks;
* [I/O](io.md) to load and serialize scenarios;
* [Adapters](adapters.md) to export models to graph libraries and databases;
* [Quickstart](quickstart.md) for a complete executable example.
