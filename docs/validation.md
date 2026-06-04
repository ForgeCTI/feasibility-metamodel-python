# Validation

Validation checks whether a scenario instantiated with the **CTI Feasibility Metamodel** is structurally correct and consistent with the metamodel.

A model may contain valid Python objects but still be invalid as a metamodel scenario. For example, a relationship may connect the wrong entity types, a relationship may point to an entity that is not part of the model, or a required cardinality may be violated.

## Purpose

Validation helps answer questions such as:

* Are all relationships connected to valid entities?
* Do relationships connect the correct source and target types?
* Are metamodel cardinalities respected?
* Are taxonomy references well formed?
* Do taxonomy references point to known taxonomy concepts?
* Are scenario files internally consistent after parsing?
* Is the model ready for analysis or export?

Validation is especially important before:

* running feasibility analysis;
* exporting to NetworkX;
* exporting to Neo4j;
* serializing a scenario;
* using a case study as reproducible evidence.

## Validation workflow

The typical workflow is:

```text
create or load scenario
        ↓
instantiate model
        ↓
validate model
        ↓
inspect validation report
        ↓
fix errors or continue with analysis/export
```

In Python:

```python
from metamodel.core.Model import Model

model = Model()

# Add entities and relationships here.

report = model.validate()

if report.is_valid:
    print("The model is valid.")
else:
    for error in report.errors:
        print(error)
```

## Validation report

Validation returns a report object.

A validation report should provide at least:

| Attribute  | Meaning                                       |
| ---------- | --------------------------------------------- |
| `is_valid` | `True` if the model has no validation errors. |
| `errors`   | List of validation errors.                    |
| `warnings` | List of non-blocking warnings, if supported.  |

Example:

```python
report = model.validate()

print(report.is_valid)
print(report.errors)
```

Possible output:

```text
False
[
    "Relationship operatesIn expects source_entity of type Organization.",
    "Cardinality violation: Organization must operate in at least one Sector."
]
```

Errors should be treated as blocking. Warnings identify issues that may not make the model invalid but should still be reviewed.

## Validation levels

The package supports several validation levels.

| Validator              | Purpose                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| Type validation        | Checks that relationship endpoints have compatible entity types.    |
| Reference validation   | Checks that relationships point to entities contained in the model. |
| Cardinality validation | Checks whether relationship multiplicities are respected.           |
| Taxonomy validation    | Checks taxonomy references, if a taxonomy registry is available.    |
| Model validation       | Runs the relevant validators on the complete model.                 |

## Type validation

Type validation checks that a relationship connects the expected source and target entity types.

For example, the relationship:

```text
operatesIn
```

should connect:

```text
Organization → Sector
```

Correct usage:

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

Incorrect usage:

```python
from metamodel.infrastructure.entities.Node import Node

node = Node(name="public-web-01")

relationship = operatesIn(
    source_entity=node,
    target_entity=sector,
)
```

This should fail because `operatesIn` does not connect `Node → Sector`.

Depending on where the check is performed, this error may be raised immediately during relationship construction or reported during model validation.

## Reference validation

Reference validation checks that relationships point to entities that belong to the model.

Example problem:

```python
from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn

model = Model()

organization = model.add_entity(Organization(name="ExampleBank"))
sector = Sector(name="Finance")  # Created but not added to the model.

model.add_relationship(
    operatesIn(
        source_entity=organization,
        target_entity=sector,
    )
)

report = model.validate()
```

In this case, the relationship points to `sector`, but `sector` was not added to the model.

Reference validation should report that the target entity is missing from the model.

Correct version:

```python
sector = model.add_entity(Sector(name="Finance"))
```

## Cardinality validation

Cardinality validation checks whether the number of relationships between entity types respects the metamodel.

Typical cardinality notation:

| Notation | Meaning       |
| -------- | ------------- |
| `1`      | Exactly one.  |
| `0..1`   | Zero or one.  |
| `1..*`   | One or more.  |
| `0..*`   | Zero or more. |

For example, if the metamodel says:

```text
Organization 1..* operatesIn Sector
```

then every `Organization` must be connected to at least one `Sector` through `operatesIn`.

Invalid example:

```python
from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization

model = Model()
organization = model.add_entity(Organization(name="ExampleBank"))

report = model.validate()
```

If `operatesIn` is mandatory for `Organization`, validation should report a cardinality violation.

Correct example:

```python
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn

sector = model.add_entity(Sector(name="Finance"))

model.add_relationship(
    operatesIn(
        source_entity=organization,
        target_entity=sector,
    )
)

report = model.validate()
```

## Cardinality direction

A relationship cardinality must be interpreted from both endpoints.

For a relationship:

```text
Organization → Sector
```

there can be two constraints:

| Side                    | Meaning                                                                    |
| ----------------------- | -------------------------------------------------------------------------- |
| Source-side cardinality | How many target entities each source entity must or may connect to.        |
| Target-side cardinality | How many source entities each target entity must or may be connected from. |

Example:

```text
Organization 1..* operatesIn Sector
Sector 0..* is operated in by Organization
```

This means:

* each `Organization` must operate in at least one `Sector`;
* a `Sector` may have zero, one, or many organizations.

## Taxonomy validation

Taxonomy validation checks taxonomy references such as:

```text
attackTools:cobaltStrike
mitreAttackEnterprise:T1190
sectors:finance
nodeTypes:webServer
```

At minimum, taxonomy validation should check the reference format:

```text
<taxonomy>:<concept>
```

Invalid examples:

```text
attackTools
attackTools:
:cobaltStrike
attackTools/cobaltStrike
```

Valid examples:

```text
attackTools:cobaltStrike
mitreAttackEnterprise:T1190
sectors:finance
```

If a taxonomy registry is available, validation can also check whether:

* the taxonomy exists;
* the concept exists;
* the concept is compatible with the entity type;
* the concept is deprecated;
* the expected taxonomy version is available.

Example:

```python
from metamodel.cyberThreat.entities.AttackTool import AttackTool

tool = AttackTool(
    name="Cobalt Strike",
    taxonomy_ref="attackTools:cobaltStrike",
)
```

If the taxonomy registry contains `attackTools:cobaltStrike`, the reference is valid.

If the registry does not contain the concept, validation should report a taxonomy error or warning.

## Attribute validation

Entities use standard Python attributes with getters and setters.

This means many errors are detected when assigning values.

Example:

```python
from metamodel.organization.entities.Organization import Organization

organization = Organization(name="ExampleBank")
organization.criticality = "critical"
```

Invalid assignment:

```python
organization.criticality = "very critical"
```

If `criticality` only accepts values such as `low`, `medium`, `high`, and `critical`, this should raise a `ValueError`.

Attribute validation usually checks:

| Check              | Example                                                          |
| ------------------ | ---------------------------------------------------------------- |
| Type               | `name` must be a string.                                         |
| Non-empty values   | `name` cannot be empty.                                          |
| Allowed values     | `criticality` must be one of a defined set.                      |
| Numeric ranges     | `cvss_score` must be between `0.0` and `10.0`.                   |
| List element types | `aliases` must contain only strings.                             |
| Date format        | Date fields should use an accepted format, such as `YYYY-MM-DD`. |
| Reference format   | `taxonomy_ref` should use `<taxonomy>:<concept>`.                |

Attribute validation protects individual entities before whole-model validation is executed.

## Structural validation

Structural validation checks the shape of the complete model.

It can detect:

* duplicate entity IDs;
* duplicate relationship IDs;
* relationships with missing endpoints;
* relationships pointing to unknown entities;
* unsupported relationship types;
* inconsistent source/target classes;
* invalid or unsupported scenario file structures.

This is especially useful after parsing a model from JSON, YAML, STIX, CSV, or draw.io.

## STIX parser validation

When a STIX bundle is parsed, the parser may produce:

* native metamodel entities;
* generic STIX entities;
* generic STIX relationships;
* skipped objects;
* skipped relationships.

For example:

```python
from metamodel.io.stixParser import loadStixBundleWithReport

result = loadStixBundleWithReport("bundle.json")

model = result.model

print(result.skipped_objects)
print(result.skipped_relationships)
```

A STIX parse result should be reviewed before using the model for analysis.

Skipped objects or relationships do not necessarily mean the bundle is invalid. They may simply indicate that no native semantic mapping has been implemented yet.

A good workflow is:

```text
parse STIX bundle
        ↓
inspect skipped objects and relationships
        ↓
validate resulting model
        ↓
decide whether custom mappers are needed
```

## Model validation after parsing

File parsers and external adapters should always be followed by validation.

Example:

```python
from metamodel.io.jsonParser import loadJsonScenario

model = loadJsonScenario("scenario.json")
report = model.validate()

if not report.is_valid:
    for error in report.errors:
        print(error)
```

For STIX:

```python
from metamodel.io.stixParser import loadStixBundleWithReport

result = loadStixBundleWithReport("bundle.json")
report = result.model.validate()

if not report.is_valid:
    for error in report.errors:
        print(error)
```

## Common validation errors

### Wrong relationship endpoint type

Problem:

```text
operatesIn received Node as source_entity instead of Organization.
```

Cause:

```text
The relationship was created with the wrong source entity type.
```

Fix:

```text
Use Organization → Sector for operatesIn.
```

### Entity not added to the model

Problem:

```text
Relationship targets an entity that is not in the model.
```

Cause:

```text
An entity object was created but not added with model.add_entity(...).
```

Fix:

```python
sector = model.add_entity(Sector(name="Finance"))
```

### Cardinality violation

Problem:

```text
Organization must operate in at least one Sector.
```

Cause:

```text
A mandatory relationship is missing.
```

Fix:

```text
Add the required relationship.
```

### Invalid taxonomy reference

Problem:

```text
taxonomy_ref must use the format '<taxonomy>:<concept>'.
```

Cause:

```text
The taxonomy reference is malformed.
```

Fix:

```text
Use attackTools:cobaltStrike instead of attackTools/cobaltStrike.
```

### Unknown taxonomy concept

Problem:

```text
Unknown taxonomy concept: attackTools:unknownTool.
```

Cause:

```text
The taxonomy registry does not contain the referenced concept.
```

Fix:

```text
Correct the concept ID or add it to the taxonomy.
```

## Validation severity

A validation system may distinguish between errors and warnings.

| Severity | Meaning                                                           |
| -------- | ----------------------------------------------------------------- |
| Error    | The model violates the metamodel and should not be used as valid. |
| Warning  | The model is usable, but something should be reviewed.            |

Examples of errors:

* wrong relationship endpoint type;
* missing mandatory relationship;
* relationship points to an entity outside the model;
* malformed taxonomy reference.

Examples of warnings:

* taxonomy concept is deprecated;
* optional recommended field is missing;
* STIX object was preserved generically instead of mapped natively;
* source field is missing for an entity derived from external information.

## Recommended validation policy

For case studies, use a strict validation policy.

Before accepting a case study:

1. Run the implementation script.
2. Validate the model.
3. Review all errors.
4. Review all warnings.
5. Export a validation report to `case_studies/<case>/output/`.
6. Document any accepted assumptions in `case_studies/<case>/notes/`.

Suggested case-study workflow:

```text
case_studies/01_case_study/
├── implementation.py
├── scenario.yaml
├── output/
│   └── validation_report.json
└── notes/
    └── assumptions.md
```

## Example validation script

```python
from pathlib import Path
import json

from case_studies.case_01.implementation import build_model

OUTPUT_FILE = Path("case_studies/01_case_study/output/validation_report.json")

model = build_model()
report = model.validate()

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", encoding="utf-8") as file:
    json.dump(
        {
            "is_valid": report.is_valid,
            "errors": report.errors,
            "warnings": getattr(report, "warnings", []),
        },
        file,
        indent=2,
    )

print(f"Validation report written to {OUTPUT_FILE}")
```

## Validation before export

Always validate before exporting.

Recommended:

```python
report = model.validate()

if not report.is_valid:
    raise RuntimeError("Cannot export an invalid model.")

graph = toNetworkx(model)
```

This avoids exporting a graph that contains broken references, invalid relationships, or incomplete mandatory structure.

## Practical checklist

Before using a scenario for analysis, check:

* Are all entities added to the model?
* Are all relationships added to the model?
* Do all relationships connect the correct entity types?
* Are mandatory relationships present?
* Are cardinality limits respected?
* Are taxonomy references well formed?
* Are taxonomy references resolvable?
* Are STIX skipped objects or relationships reviewed?
* Are assumptions documented?
* Does `model.validate()` return `is_valid = True`?

## Next steps

Continue with:

* [I/O](io.md) to understand scenario loading and serialization;
* [Adapters](adapters.md) to export validated models;
* [Taxonomies](taxonomies.md) to understand taxonomy reference validation;
* [Metamodel](metamodel.md) to review entity and relationship semantics.
