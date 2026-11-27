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

These sub-metamodels are connected through relationships. The default Registry currently defines 39 entity classes and 62 relationship classes. For example, a threat step can target an infrastructure resource, exploit a vulnerability, and compromise a security requirement associated with an organizational asset.

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
| Python attributes  | Snake case                  | `external_id`, `ip_addresses` |

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
* an optional `source` attribute.

The internal identifier is generated automatically and should not be manually assigned by the user.

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
* cardinality metadata.

Relationships do not include a traceability `source` attribute. Traceability is stored at the entity level when needed.

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

A cardinality of `None` means that no constraint has been specified; it is distinct from an explicit `"0..*"` constraint. Cardinality validation is performed at the model level because it requires knowledge of all entities and relationships in a scenario.

```python
report = model.validate()

if not report.is_valid:
    for error in report.errors:
        print(error)
```

## Organization sub-metamodel

The organization sub-metamodel represents the organizational context in which feasibility is assessed.

It captures the organization, its sector, jurisdictional context, business requirements, security requirements, and assets.

### Organization entities

| Entity                     | Description                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `Organization`             | The organization being modelled or assessed.                      |
| `Sector`                   | Economic, industrial, or institutional sector.                    |
| `HomeCountry`              | Country where the organization is based.                          |
| `InternationalBody`        | Supranational or international body relevant to the organization. |
| `BusinessRequirement`      | Business requirement that drives organizational priorities.       |
| `SecurityRequirement`      | Generic security requirement or control objective.                |
| `Asset`                    | Organizational asset with business value.                         |
| `AssetSecurityRequirement` | Security requirement associated with a specific asset.            |

### Typical organization relationships

| Relationship             | Meaning                                                            |
| ------------------------ | ------------------------------------------------------------------ |
| `operatesIn`             | Connects an `Organization` to a `Sector`.                          |
| `basedIn`                | Connects an `Organization` to a `HomeCountry`.                     |
| `hasBusinessRequirement` | Connects an `Organization` to a `BusinessRequirement`.             |
| `countryPartOf`          | Connects a `HomeCountry` to an `InternationalBody`.                |
| `drivesSecurityRequirement`      | Connects a `BusinessRequirement` to an `AssetSecurityRequirement`. |
| `hasSecurityRequirement`    | Connects an `Asset` to an `AssetSecurityRequirement`.              |
| `implementsRequirement`  | Connects an `AssetSecurityRequirement` to a `SecurityRequirement`. |

The organization sub-metamodel is important because feasibility is not only technical. A threat may be technically possible but more or less relevant depending on the organization’s sector, assets, requirements, and exposure.

## Infrastructure sub-metamodel

The infrastructure sub-metamodel represents the technical environment in which threat feasibility is evaluated.

It captures nodes, users, ports, connections, applications, operating systems, code, information, and resources.

### Infrastructure entities

| Entity                | Description                                                     |
| --------------------- | --------------------------------------------------------------- |
| `Infrastructure`      | Infrastructure scope managed by an organization.                |
| `Node`                | Host, server, endpoint, device, or logical infrastructure node. |
| `NodeType`            | Type or category of node.                                       |
| `Port`                | Network port or exposed service endpoint.                       |
| `Connection`          | Network or logical connection between nodes.                    |
| `Resource`            | Infrastructure resource relevant to the organization or threat. |
| `Code`                | Software code, script, service logic, or executable component.  |
| `Information`         | Information object or data item.                                |
| `InformationType`     | Type or classification of information.                          |
| `User`                | Human or account-level actor in the infrastructure.             |
| `UserType`            | Category of user.                                               |
| `Application`         | Generic application or software product.                        |
| `ApplicationInstance` | Concrete installed or running application instance.             |
| `OS`                  | Generic operating system.                                       |
| `OSInstance`          | Concrete installed or running operating system instance.        |

### Typical infrastructure relationships

| Relationship              | Meaning                                                                               |
| ------------------------- | ------------------------------------------------------------------------------------- |
| `manages`                 | Connects an `Organization` to an `Infrastructure`.                                    |
| `madeBy`                  | Connects an `Infrastructure` to a `Node`.                                             |
| `usedBy`                  | Connects an `Infrastructure` to a `User`.                                             |
| `hasNodeType`             | Connects a `Node` to a `NodeType`.                                                    |
| `hostsResource`           | Connects a `Node` to a `Resource`.                                                    |
| `exposesPort`             | Connects a `Node` to a `Port`.                                                        |
| `isSource`                | Connects a source `Node` to a `Connection`.                                           |
| `isDestination`           | Connects a destination `Node` to a `Connection`.                                      |
| `hasDestinationPort`         | Connects a `Connection` to a destination `Port`.                                      |
| `runsOS`                  | Connects a `Node` to an `OSInstance`.                                                 |
| `osInstanceOf`            | Connects an `OSInstance` to an `OS`.                                                  |
| `runsApp`         | Connects a `Node` to an `ApplicationInstance`.                                        |
| `applicationInstanceOf`   | Connects an `ApplicationInstance` to an `Application`.                                |
| `resourceImplementsCode`    | Connects a `Resource` to `Code`.                              |
| `applicationImplementsCode` | Connects an `ApplicationInstance` to `Code`.                   |
| `resourceImplementsAsset`         | Connects a `Resource` to an organizational `Asset`.                                   |
| `accessesInformation`     | Connects `Code` to `Information`.                                                     |
| `listensOn`               | Connects `Code` to a `Port`.                                                          |
| `hasInformationType`      | Connects `Information` to an `InformationType`.                                       |
| `hasAccessTo`             | Connects a `User` to a `Node`.                                                        |
| `launches`                | Connects a `User` to `Code`.                                                          |
| `userAccessesInformation` | Connects a `User` to `Information`.                                                   |
| `hasUserType`             | Connects a `User` to a `UserType`.                                                    |
| `runs`                | Connects a `Node` to another `Node` when nested or virtualized execution is modelled. |

The infrastructure sub-metamodel is the main bridge between abstract CTI and concrete feasibility. It represents whether the technical conditions required by a threat step are present in the scenario.

## Cyber-threat sub-metamodel

The cyber-threat sub-metamodel represents CTI concepts relevant to feasibility analysis.

It captures adversaries, threat actors, campaigns, threats, attack steps, TTPs, vulnerabilities, indicators, attack tools, and configurations.

### Cyber-threat entities

| Entity                    | Description                                                      |
| ------------------------- | ---------------------------------------------------------------- |
| `ThreatActor`             | Actor or group associated with threat activity.                  |
| `Adversary`               | Adversarial profile, capability, or intent abstraction.          |
| `AdversaryType`           | Category of adversary.                                           |
| `Expertise`               | Skill or expertise level required or possessed.                  |
| `Threat`                  | Threat scenario or high-level malicious activity.                |
| `ThreatStep`              | Step in a threat or attack chain.                                |
| `Campaign`                | Coordinated set of threat activities.                            |
| `TTP`                     | Tactic, technique, or procedure.                                 |
| `Indicator`               | Observable indicator associated with threat activity.            |
| `Vulnerability`           | Generic vulnerability concept.                                   |
| `SoftwareVulnerability`   | Vulnerability affecting software or platforms.                   |
| `ConfigVulnerability`     | Vulnerability caused by misconfiguration.                        |
| `HumanVulnerability`      | Vulnerability involving users or human behavior.                 |
| `AttackTool`              | Generic attack tool, malware family, exploit kit, or capability. |
| `AttackToolInstance`      | Concrete observed or deployed instance of an attack tool.        |
| `AttackToolConfiguration` | Configuration of an attack tool instance.                        |

### Typical cyber-threat relationships

| Relationship               | Meaning                                                           |
| -------------------------- | ----------------------------------------------------------------- |
| `relatedTo`                | Connects a `ThreatActor` to an `Adversary`.                       |
| `aliasOf`                  | Connects one `ThreatActor` alias to another.                      |
| `initiates`                | Connects a `ThreatActor` to a `Threat`.                           |
| `hasExpertise`             | Connects a `ThreatActor` to `Expertise`.                  |
| `hasAdversaryType`         | Connects an `Adversary` to an `AdversaryType`.                    |
| `threatPartOf`             | Connects a `Threat` to a `Campaign`.                              |
| `startsWith`               | Connects a `Threat` to its first `ThreatStep`.                    |
| `followedBy`               | Connects one `ThreatStep` to a following `ThreatStep`.            |
| `implementsTTP`            | Connects a `ThreatStep` to a `TTP`.                               |
| `exploits`                 | Connects a `ThreatStep` to a `Vulnerability`.                     |
| `compromises`              | Connects a `ThreatStep` to an `AssetSecurityRequirement`.         |
| `targetsResource`          | Connects a `ThreatStep` to a `Resource`.                          |
| `employsTool`              | Connects a `ThreatStep` to an `AttackToolInstance`.               |
| `exploitsVulnerability`              | Connects a `TTP` to a `Vulnerability`.                            |
| `violates`                 | Connects a `TTP` to a `SecurityRequirement`.                      |
| `targetsSector`            | Connects a `Campaign` to a `Sector`.                              |
| `focusesOnCountry`         | Connects a `Campaign` to a `HomeCountry`.                         |
| `targetsInternationalBody`              | Connects a `Campaign` to an `InternationalBody`.                  |
| `producesIndicator`        | Connects an `AttackToolInstance` to an `Indicator`.               |
| `associatedToTool`         | Connects an `Indicator` to an `AttackToolInstance`.               |
| `toolInstanceOf`           | Connects an `AttackToolInstance` to an `AttackTool`.              |
| `hasConfig`            | Connects an `AttackToolInstance` to an `AttackToolConfiguration`. |
| `designedFor`              | Connects an `AttackToolInstance` to an `OSInstance`.              |
| `deploysTool`              | Connects one `AttackToolInstance` to another deployed instance.   |
| `deployedTo`               | Connects an `AttackToolInstance` to a `Node`.                     |
| `requiresConfig`           | Connects an `AttackTool` to an `AttackToolConfiguration`.         |
| `requiresExpertise`        | Connects an `AttackTool` to `Expertise`.                          |
| `affectsApplication`       | Connects `SoftwareVulnerability` to an `Application`.             |
| `affectsOS`                | Connects `SoftwareVulnerability` to an `OS`.                      |
| `affectsCode`              | Connects `ConfigVulnerability` to `Code`.                         |
| `affectsUser`              | Connects `HumanVulnerability` to a `User`.                        |

The cyber-threat sub-metamodel captures CTI knowledge in a form that can be checked against a concrete organization and infrastructure.

## Cross-sub-metamodel relationships

The metamodel is useful because the three sub-metamodels are connected.

Examples:

```text
Organization → Infrastructure
Resource → Asset
ThreatStep → Resource
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

Resource
    implements Asset
    hosted on Node

Node
    exposes Port
    runs OSInstance
    runs ApplicationInstance

Asset
    has AssetSecurityRequirement
```

This allows a threat step to be evaluated against actual infrastructure conditions and organizational requirements.

## Taxonomies

The repository includes taxonomy support for reusable controlled vocabularies. However, the current domain entity classes no longer expose a `taxonomy_ref` attribute, and `Model.validate()` does not validate taxonomy references.

A taxonomy is not the same as a scenario instance.

```text
Taxonomy concept:
  generic reusable knowledge

Scenario instance:
  concrete object in a specific model
```

For example, an `AttackTool` can be instantiated without a taxonomy reference:

```python
from metamodel.cyberThreat.entities.AttackTool import AttackTool

tool = AttackTool(name="Cobalt Strike")
```

A `TTP` can record an external MITRE ATT&CK technique identifier in its `external_id` attribute:

```python
from metamodel.cyberThreat.entities.TTP import TTP

ttp = TTP(
    name="Exploit Public-Facing Application",
    external_id="T1190",
)
```

The taxonomy module uses references in the format:

```text
<taxonomy>:<concept>
```

Examples of taxonomy identifiers (not entity constructor arguments):

```text
attackTools:cobaltStrike
mitreAttackEnterprise:T1190
cve:CVE-2026-0001
sectors:finance
nodeTypes:webServer
userTypes:administrator
informationTypes:personalData
```

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

```python
from metamodel.core.Model import Model

model = Model()

model.add(entity)
model.add(relationship)
```

The model is responsible for whole-scenario operations such as validation and serialization. `Model.add()` accepts only entity and relationship classes defined in its Registry. To extend the default metamodel, new classes must also be listed in `registry_data.py`, which is loaded by `Registry.load_default()`.

```python
report = model.validate()
```

## Validation

The metamodel supports several validation levels.

| Validation type        | Purpose                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| Type validation        | Checks registered classes and compatible relationship endpoint types. |
| Reference validation   | Checks that relationship endpoints belong to the model.              |
| Uniqueness validation  | Checks duplicate relationship IDs and directed connections.         |
| Cardinality validation | Checks relationship multiplicities and reports isolated entities.   |
| Model validation       | Coordinates validation and aggregates the results.                  |

Model validation runs structural checks (references, types and uniqueness) first. Cardinality checks run only if no structural errors are found. Validation returns a report.

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
Resource: Customer web portal
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
public-web-01 hostsResource Customer web portal
Example actor initiates Web portal compromise
Web portal compromise startsWith Exploit public-facing web application
Exploit public-facing web application implementsTTP Exploit Public-Facing Application
Exploit public-facing web application exploits CVE-like vulnerability
Exploit public-facing web application targetsResource Customer web portal
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

## UML diagram generation

The repository provides a Python script, `scripts/generate_uml.py`, for generating two complementary UML views of the metamodel:

* **Metamodel Entity Structure:** represents the entities of the three sub-metamodels, their domain attributes, and inheritance hierarchies.
* **Complete Metamodel Class Diagram:** additionally represents relationships between entities and their declared cardinalities.

The diagrams are generated directly from the Python implementation. Entity classes, domain attributes, attribute types, inheritance hierarchies, relationships, and cardinalities are extracted from the registered classes.

The reference file `docs/diagrams/metamodel_v2.drawio`, specifically its `Leonardo's touch` page, provides the class positions used to generate the complete diagram. Relationship paths are computed independently of the connectors defined in the reference file.

### Generating the diagrams

Run the following command from the repository root:

```bash
python scripts/generate_uml.py --src src --reference docs/diagrams/metamodel_v2.drawio --output-dir docs/diagrams
```

The generator uses only Python standard-library modules and does not require additional third-party dependencies.

The following files are generated in `docs/diagrams/`:

| File | Description |
| --- | --- |
| `metamodel_entities.drawio` | Editable entity structure diagram. |
| `metamodel_entities.svg` | Vector representation of the entity structure. |
| `metamodel_complete.drawio` | Editable complete class diagram. |
| `metamodel_complete.svg` | Vector representation of the complete class diagram. |

### Keeping the diagrams up to date

When extending or modifying the metamodel:

1. Update the Python implementation and register any new entity or relationship classes in `src/metamodel/registry_data.py`.
2. Update the reference diagram `metamodel_v2.drawio` to maintain consistency with the conceptual metamodel.
3. When adding or renaming an entity, ensure that a uniquely named corresponding class is present in the `Leonardo's touch` page, with sufficient space around neighbouring classes.
4. Run the UML generation script again.
5. Review the generated diagrams for correctness and readability.

Changes to domain attributes, attribute types, inheritance hierarchies, relationships, and cardinalities are extracted from the Python implementation and do not require manual editing of the generated diagrams.

Although new relationships are extracted directly from the registered Python classes, the reference diagram should also be updated to remain consistent with the conceptual metamodel.

The generator is designed around the current metamodel structure. Significant extensions may require adjustments to the reference layout or to the generation algorithm, particularly when class dimensions, relationship density, or domain organization change.

## Next steps

Continue with:

* [Taxonomies](taxonomies.md) to understand controlled vocabulary integration;
* [Validation](validation.md) to understand model correctness checks;
* [I/O](io.md) to load and serialize scenarios;
* [Adapters](adapters.md) to export models to graph libraries and databases;
* [Quickstart](quickstart.md) for a complete executable example.
