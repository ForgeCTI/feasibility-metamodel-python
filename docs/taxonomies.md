# Taxonomies

The **CTI Feasibility Metamodel** supports taxonomies to represent reusable controlled vocabularies.

Taxonomies are used to connect scenario-specific model instances to standardized or project-specific reference knowledge, such as attack tools, TTPs, vulnerabilities, node types, sectors, countries, platforms, and security requirements.

## Purpose

A metamodel scenario contains concrete instances.

For example:

```text
AttackTool: Cobalt Strike observed in a campaign
Node: public-web-01
Sector: Finance
TTP: Exploit Public-Facing Application
```

A taxonomy contains reusable concepts.

For example:

```text
attackTools:cobaltStrike
nodeTypes:webServer
sectors:finance
mitreAttackEnterprise:T1190
```

The distinction is important:

| Layer             | Meaning                              | Example                            |
| ----------------- | ------------------------------------ | ---------------------------------- |
| Taxonomy concept  | Reusable reference knowledge         | `attackTools:cobaltStrike`         |
| Metamodel entity  | Entity type defined by the metamodel | `AttackTool`                       |
| Scenario instance | Concrete object in a model           | `AttackTool(name="Cobalt Strike")` |

A taxonomy reference allows a scenario instance to point to a reusable concept without hardcoding large catalogues into entity classes.

## Recommended reference format

The recommended format for taxonomy references is:

```text
<taxonomy>:<concept>
```

Examples:

```text
attackTools:cobaltStrike
mitreAttackEnterprise:T1190
cve:CVE-2026-0001
cwe:CWE-79
sectors:finance
countries:IT
nodeTypes:webServer
userTypes:administrator
informationTypes:personalData
securityRequirements:confidentiality
```

The part before `:` identifies the taxonomy.
The part after `:` identifies the concept within that taxonomy.

## Where taxonomies are stored

Taxonomies are stored under:

```text
src/metamodel/taxonomies/
```

Recommended organization:

```text
src/metamodel/taxonomies/
├── __init__.py
├── Taxonomy.py
├── TaxonomyConcept.py
├── TaxonomyMapping.py
├── TaxonomyRegistry.py
│
├── attackTools/
│   ├── attackTools.yaml
│   ├── aliases.yaml
│   ├── categories.yaml
│   ├── externalReferences.yaml
│   └── loader.py
│
├── ttps/
│   ├── mitreAttackEnterprise.yaml
│   ├── mitreAttackMobile.yaml
│   ├── mitreAttackIcs.yaml
│   └── loader.py
│
├── vulnerabilities/
│   ├── cwe.yaml
│   ├── capec.yaml
│   └── loader.py
│
├── platforms/
│   ├── operatingSystems.yaml
│   ├── applications.yaml
│   ├── cloudServices.yaml
│   └── loader.py
│
├── infrastructure/
│   ├── nodeTypes.yaml
│   ├── userTypes.yaml
│   ├── informationTypes.yaml
│   └── loader.py
│
└── organization/
    ├── sectors.yaml
    ├── countries.yaml
    ├── internationalBodies.yaml
    ├── securityRequirements.yaml
    └── loader.py
```

Taxonomy files should be small enough to maintain, but structured enough to support validation, lookup, aliases, categories, and external references.

## Taxonomy concept structure

A taxonomy concept should have a stable identifier and human-readable metadata.

Example:

```yaml
id: cobaltStrike
name: Cobalt Strike
category: command_and_control
description: Commercial adversary simulation framework frequently abused by threat actors.
aliases:
  - Beacon
external_references:
  - source: mitre_attack_software
    external_id: S0154
capabilities:
  - command_and_control
  - lateral_movement
  - credential_access
```

Recommended fields:

| Field                 | Required | Meaning                                         |
| --------------------- | -------: | ----------------------------------------------- |
| `id`                  |      Yes | Stable concept identifier within the taxonomy.  |
| `name`                |      Yes | Human-readable concept name.                    |
| `description`         |       No | Textual description.                            |
| `category`            |       No | Category or family of the concept.              |
| `aliases`             |       No | Alternative names.                              |
| `external_references` |       No | References to external catalogues or standards. |
| `tags`                |       No | Generic labels for filtering and lookup.        |
| `properties`          |       No | Additional taxonomy-specific fields.            |

## Taxonomy file structure

A taxonomy file should include metadata and a list of concepts.

Example:

```yaml
taxonomy:
  id: attackTools
  name: Attack tools
  version: "0.1"
  source: "Project-maintained taxonomy"
  description: "Controlled vocabulary for attack tools."

concepts:
  - id: cobaltStrike
    name: Cobalt Strike
    category: command_and_control
    description: Commercial adversary simulation framework frequently abused by threat actors.
    aliases:
      - Beacon
    external_references:
      - source: mitre_attack_software
        external_id: S0154
    capabilities:
      - command_and_control
      - lateral_movement
      - credential_access

  - id: mimikatz
    name: Mimikatz
    category: credential_tool
    description: Tool commonly used to extract credentials from Windows systems.
    aliases: []
    external_references:
      - source: mitre_attack_software
        external_id: S0002
    capabilities:
      - credential_access
```

The taxonomy identifier is:

```text
attackTools
```

The complete references are:

```text
attackTools:cobaltStrike
attackTools:mimikatz
```

## Using taxonomy references in entities

Taxonomy-backed entities can include a `taxonomy_ref` domain attribute.

Example:

```python
from metamodel.cyberThreat.entities.AttackTool import AttackTool

tool = AttackTool(
    name="Cobalt Strike",
    taxonomy_ref="attackTools:cobaltStrike",
    aliases=["Beacon"],
    tool_type="command_and_control",
    capabilities=["command_and_control", "lateral_movement"],
    source="Example taxonomy"
)
```

The entity is still a scenario object. The taxonomy reference connects it to reusable knowledge.

## Typical taxonomy-backed entities

The following entities are strong candidates for taxonomy references.

| Entity                  | Example taxonomy reference                    |
| ----------------------- | --------------------------------------------- |
| `AttackTool`            | `attackTools:cobaltStrike`                    |
| `TTP`                   | `mitreAttackEnterprise:T1190`                 |
| `Vulnerability`         | `cve:CVE-2026-0001`                           |
| `SoftwareVulnerability` | `cve:CVE-2026-0001`                           |
| `ConfigVulnerability`   | `misconfigurations:weakAccessControl`         |
| `HumanVulnerability`    | `humanVulnerabilities:phishingSusceptibility` |
| `NodeType`              | `nodeTypes:webServer`                         |
| `UserType`              | `userTypes:administrator`                     |
| `InformationType`       | `informationTypes:personalData`               |
| `Sector`                | `sectors:finance`                             |
| `HomeCountry`           | `countries:IT`                                |
| `InternationalBody`     | `internationalBodies:EU`                      |
| `SecurityRequirement`   | `securityRequirements:confidentiality`        |
| `Application`           | `applications:apacheHttpServer`               |
| `OS`                    | `operatingSystems:windowsServer`              |

Not every entity needs a taxonomy reference. For example, `Node`, `User`, `ThreatStep`, or `AttackToolInstance` are usually scenario-specific and may not need taxonomy references.

## Taxonomies and scenario instances

Taxonomies should not replace scenario instances.

For example, this is a taxonomy concept:

```text
attackTools:cobaltStrike
```

This is a scenario instance:

```python
AttackTool(
    name="Cobalt Strike",
    taxonomy_ref="attackTools:cobaltStrike"
)
```

This is a concrete observed instance:

```python
AttackToolInstance(
    name="Cobalt Strike Beacon observed in case study 1",
    observed_version="unknown",
    hashes=["..."]
)
```

The relationship between generic and concrete tool knowledge should be modelled explicitly:

```text
AttackToolInstance → toolInstanceOf → AttackTool
```

This separation allows the same taxonomy concept to be reused across many scenarios.

## Taxonomy validation

Taxonomy validation checks whether taxonomy references are well-formed and resolvable.

Validation can check:

| Check              | Meaning                                                     |
| ------------------ | ----------------------------------------------------------- |
| Format             | Does the reference use `<taxonomy>:<concept>`?              |
| Taxonomy existence | Does the taxonomy exist in the registry?                    |
| Concept existence  | Does the concept exist in the selected taxonomy?            |
| Compatibility      | Is the taxonomy allowed for this entity type?               |
| Deprecation        | Is the referenced concept deprecated?                       |
| Version            | Was the concept available in the expected taxonomy version? |

Example invalid references:

```text
attackTools
attackTools:
:cobaltStrike
attackTools:unknownTool
mitreAttackEnterprise
```

Example valid references:

```text
attackTools:cobaltStrike
mitreAttackEnterprise:T1190
sectors:finance
countries:IT
```

## Minimal taxonomy registry

The package can maintain a taxonomy registry that loads and indexes concepts.

Conceptual example:

```python
from metamodel.taxonomies.TaxonomyRegistry import TaxonomyRegistry

registry = TaxonomyRegistry()

registry.load_yaml("src/metamodel/taxonomies/attackTools/attackTools.yaml")
registry.load_yaml("src/metamodel/taxonomies/organization/sectors.yaml")

concept = registry.get("attackTools:cobaltStrike")

print(concept.name)
```

The registry should support:

* loading taxonomy files;
* lookup by full reference;
* lookup by taxonomy and concept id;
* lookup by alias;
* checking whether a reference exists;
* checking whether a reference is compatible with an entity type.

## Example: attack tool taxonomy

A small attack-tool taxonomy can be represented as:

```yaml
taxonomy:
  id: attackTools
  name: Attack tools
  version: "0.1"
  source: "Example local taxonomy"

concepts:
  - id: cobaltStrike
    name: Cobalt Strike
    category: command_and_control
    description: Commercial adversary simulation framework frequently abused by threat actors.
    aliases:
      - Beacon
    capabilities:
      - command_and_control
      - lateral_movement
      - credential_access
```

The concept can then be used in a model:

```python
from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.AttackTool import AttackTool

model = Model()

tool = model.add_entity(
    AttackTool(
        name="Cobalt Strike",
        taxonomy_ref="attackTools:cobaltStrike",
        aliases=["Beacon"],
        tool_type="command_and_control",
        capabilities=[
            "command_and_control",
            "lateral_movement",
            "credential_access",
        ],
    )
)
```

## Example: TTP taxonomy

A TTP can reference a MITRE ATT&CK-like taxonomy concept:

```python
from metamodel.cyberThreat.entities.TTP import TTP

ttp = TTP(
    name="Exploit Public-Facing Application",
    taxonomy_ref="mitreAttackEnterprise:T1190",
    external_id="T1190",
    tactic="initial_access",
    technique="Exploit Public-Facing Application",
)
```

This does not require the whole external taxonomy to be hardcoded into the `TTP` class. The entity only stores the reference.

## External references

Taxonomy concepts can store references to external catalogues.

Example:

```yaml
external_references:
  - source: mitre_attack_enterprise
    external_id: T1190
    url: https://attack.mitre.org/techniques/T1190/

  - source: cwe
    external_id: CWE-79
    url: https://cwe.mitre.org/data/definitions/79.html
```

External references are useful for:

* linking to authoritative sources;
* mapping between taxonomies;
* preserving provenance;
* exporting to graph databases;
* documentation generation.

## Taxonomy aliases

Aliases allow flexible lookup.

Example:

```yaml
id: cobaltStrike
name: Cobalt Strike
aliases:
  - Beacon
  - CobaltStrike
```

A registry can use aliases to resolve:

```text
Beacon → attackTools:cobaltStrike
CobaltStrike → attackTools:cobaltStrike
```

Aliases are especially useful for CTI sources where different names are used for the same tool, malware family, technique, or actor.

## Taxonomy mappings

Sometimes two taxonomies describe related concepts.

Example:

```yaml
source:
  taxonomy: attackTools
  concept: cobaltStrike

target:
  taxonomy: mitreAttackSoftware
  concept: S0154

mapping_type: exact
```

Possible mapping types:

| Mapping type | Meaning                                         |
| ------------ | ----------------------------------------------- |
| `exact`      | Concepts refer to the same thing.               |
| `close`      | Concepts are similar but not identical.         |
| `broader`    | Source concept is broader than target concept.  |
| `narrower`   | Source concept is narrower than target concept. |
| `related`    | Concepts are related but not hierarchical.      |

Mappings are useful when integrating internal taxonomies with external CTI sources.

## Versioning

Taxonomies should be versioned.

Example:

```yaml
taxonomy:
  id: attackTools
  version: "2026.1"
```

Versioning matters because taxonomies evolve. Concepts may be added, renamed, split, merged, or deprecated.

Recommended versioning rules:

| Rule                     | Recommendation                                           |
| ------------------------ | -------------------------------------------------------- |
| Stable concept IDs       | Avoid changing concept IDs once released.                |
| Deprecated concepts      | Keep deprecated concepts with a `deprecated: true` flag. |
| Replacement references   | Use `replaced_by` when a concept is superseded.          |
| Changelog                | Track taxonomy changes in documentation or metadata.     |
| Scenario reproducibility | Store taxonomy version used by a case study.             |

Example deprecated concept:

```yaml
id: oldToolName
name: Old Tool Name
deprecated: true
replaced_by: attackTools:newToolName
```

## Taxonomies and STIX

The STIX parser can map STIX objects into native metamodel entities where possible.

For example:

| STIX object type | Native entity   | Possible taxonomy reference |
| ---------------- | --------------- | --------------------------- |
| `attack-pattern` | `TTP`           | `mitre_attack:T1059`        |
| `tool`           | `AttackTool`    | `stixTool:<stix-id>`        |
| `malware`        | `AttackTool`    | `stixMalware:<stix-id>`     |
| `vulnerability`  | `Vulnerability` | `cve:CVE-2026-0001`         |
| `indicator`      | `Indicator`     | Usually scenario-specific   |

If a STIX object has external references, the parser can use them to construct taxonomy references.

Example:

```json
{
  "type": "attack-pattern",
  "name": "Command and Scripting Interpreter",
  "external_references": [
    {
      "source_name": "mitre-attack",
      "external_id": "T1059"
    }
  ]
}
```

Possible taxonomy reference:

```text
mitre_attack:T1059
```

This allows STIX-derived entities to remain connected to external CTI catalogues.

## Recommended taxonomy design

When designing a taxonomy, prefer:

* stable IDs;
* concise concept names;
* explicit categories;
* aliases for CTI naming variation;
* external references where available;
* version metadata;
* deprecation metadata;
* mappings to external taxonomies when useful.

Avoid:

* using long descriptions as identifiers;
* changing IDs after publication;
* mixing scenario-specific observations with reusable concepts;
* encoding relationships that should belong to the metamodel;
* storing large unstructured notes inside taxonomy concepts.

## Minimal checklist

A good taxonomy should answer:

* What is the taxonomy ID?
* What version is it?
* Who maintains it?
* What concepts does it define?
* Are concept IDs stable?
* Are aliases included?
* Are external references included?
* Are deprecated concepts marked?
* Can scenario entities reference it with `<taxonomy>:<concept>`?

## Next steps

Continue with:

* [Validation](validation.md) to understand taxonomy validation and model validation;
* [I/O](io.md) to load taxonomy-backed scenarios from files;
* [Adapters](adapters.md) to export taxonomy references to NetworkX or Neo4j;
* [Metamodel](metamodel.md) for the entities that can use taxonomy references.
