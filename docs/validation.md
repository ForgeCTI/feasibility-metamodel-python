# Validation

Validation verifies that a scenario built with the **CTI Feasibility Metamodel** satisfies the structural constraints defined by the metamodel. A model can contain correctly instantiated Python objects and still violate constraints involving references, relationship types, uniqueness or cardinalities.

Validation establishes **structural consistency**, not the feasibility of a cyber-attack. It should be performed before using a scenario for subsequent analysis or export.

## Running validation

Create a `Model`, add its entities and relationships, and call `validate()`:

```python
from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Expertise import Expertise
from metamodel.cyberThreat.rels.hasExpertise import hasExpertise

model = Model()
actor = model.add(ThreatActor(name="Actor"))
expertise = model.add(Expertise(name="Expertise"))
model.add(hasExpertise(actor, expertise))

report = model.validate()

print("Valid:", report.is_valid)
for item in report.messages:
    print(f"[{item.severity}] {item.validator}: {item.message}")
```

This model is valid and produces no validation messages. If the `hasExpertise` relationship is omitted, the report contains two cardinality errors and two isolated-entity warnings.

## Validation architecture

`Model.validate()` delegates to `validateModel()`, which **coordinates the validators and aggregates their reports**. Validation proceeds in two stages:

| Stage | Validator | Responsibility |
| --- | --- | --- |
| 1 — Structural | `referenceValidator` | Verify that relationship endpoints belong to the model. |
| 1 — Structural | `typeValidator` | Verify registered classes and compatible endpoint types. |
| 1 — Structural | `uniquenessValidator` | Detect duplicate relationship UUIDs and duplicate directed connections. |
| 2 — Cardinality | `cardinalityValidator` | Enforce relationship cardinalities and report isolated entities. |

All three structural validators run, and their errors are collected in the same report. **The Cardinality Validator runs only if there are no structural errors**, avoiding misleading counts on inconsistent relationships.

An entirely empty model produces a warning from `modelValidator`, but no error. Warnings alone do not make a model invalid.

### Preventive checks and model validation

The public API prevents several invalid states before validation:

- `BaseRelationship` checks endpoint type compatibility when a relationship is constructed.
- `Model.add()` accepts only entity and relationship classes registered in the metamodel; it also checks relationship endpoint membership and uniqueness.
- `Model.update_relationship()` validates updated endpoints and prevents duplicate connections.

The validators check the **resulting model** independently. They can therefore detect structural inconsistencies introduced by bypassing public methods or altering internal state. Such direct manipulation is intended only for controlled tests and demonstrations; see [Invalid Model](../examples/15_invalid_model/README.md).

## Structural validation rules

### Type validation

The `typeValidator` checks two distinct conditions:

1. **Registration:** every entity and relationship must be an instance of the exact class registered for its type. The default `Registry` loads these definitions from `registry_data.py`; matching a registered class name alone is insufficient.
2. **Endpoint compatibility:** each registered relationship must connect instances compatible with its declared `source_type` and `target_type`. Compatibility uses `isinstance()`, so appropriate entity subclasses are supported.

For example, `operatesIn` connects `Organization` to `Sector`. Constructing it with a `Node` as the source raises `TypeError`. If a registered relationship is corrupted after construction, the Type Validator can report an invalid endpoint type. Relationships with undefined endpoint types are also reported as errors.

To extend the default metamodel, new entity or relationship classes must be declared in the corresponding modules **and registered in `registry_data.py`**.

### Reference validation

The `referenceValidator` verifies that the source and target of every relationship refer to entities contained in the model, comparing their UUIDs with the IDs of registered model entities.

For instance, creating `operatesIn(organization, sector)` is allowed when both endpoints have compatible types, but `Model.add()` rejects that relationship if `sector` has not been added to the model. The Reference Validator detects the same missing reference if insertion checks have been bypassed.

### Uniqueness validation

The `uniquenessValidator` enforces two rules:

- Relationship UUIDs must be unique within a model.
- A directed connection, identified by `(relationship type, source UUID, target UUID)`, must not occur twice, even if the two relationship instances have different UUIDs.

Endpoint order matters: `aliasOf(A, B)` and `aliasOf(B, A)` are treated as different directed connections. The validator does not infer a symmetry constraint from the relationship name.

`Model.add()` and `Model.update_relationship()` prevent duplicates during normal use. The Uniqueness Validator detects them in an already constructed or intentionally corrupted model.

## Cardinality validation

Each relationship class may define `source_cardinality` and `target_cardinality`. These values are interpreted using the `Cardinality` class.

| Notation | Meaning |
| --- | --- |
| `1` | Exactly one. |
| `0..1` | Zero or one. |
| `1..*` | One or more. |
| `0..*` | Zero or more. |
| `None` | No constraint declared for that side. |

`None` and `"0..*"` are **not equivalent**: one leaves the constraint unspecified, whereas the other explicitly allows any non-negative count.

### Cardinality direction

For `Organization --operatesIn--> Sector`, the class declares:

```python
source_cardinality = "1"
target_cardinality = "1..*"
```

The directions are interpreted as follows:

| Attribute | Constraint |
| --- | --- |
| `source_cardinality` | Number of **source** entities per **target** entity: each `Sector` must be associated with exactly one `Organization`. |
| `target_cardinality` | Number of **target** entities per **source** entity: each `Organization` must be associated with at least one `Sector`. |

The Cardinality Validator checks the constraints of **all registered relationship classes**, including types for which no relationship instance is present. Missing mandatory relationships therefore count as zero and produce errors. Compatible subclasses are included through `isinstance()`.

An entity not involved in any relationship also produces an **isolated-entity warning**. Isolation does not invalidate a model by itself, although the entity may independently violate a mandatory cardinality.

## Local attribute validation

Entity constructors and property setters enforce local attribute constraints, separately from `Model.validate()`. Depending on the attribute, these include required strings, data types, IP/MAC address formats, and chronological consistency between dates (for example, `first_seen` and `last_seen`). Invalid assignments normally raise an exception at the point of assignment.

Not all descriptive attributes are restricted to enumerations. In particular, `Organization.criticality` accepts a free-form string in the current implementation.

## Validation reports

`Model.validate()` returns a `ValidationReport` with the following read-only accessors:

| Property | Meaning |
| --- | --- |
| `messages` | All validation messages. |
| `errors` | Messages with severity `"error"`. |
| `warnings` | Messages with severity `"warning"`. |
| `is_valid` | `True` if no errors were reported. |

Each entry is an immutable `ValidationMessage` with three attributes: `validator`, `message` and `severity`. The report provides `add_error()`, `add_warning()` and `extend()` to collect messages; the public message lists are returned as copies.

```python
report = model.validate()

print("Valid:", report.is_valid)
print("Errors:", len(report.errors))
print("Warnings:", len(report.warnings))

for error in report.errors:
    print(f"{error.validator}: {error.message}")
```

An error makes `is_valid` false. Warnings do not. Cardinality errors and isolated-entity warnings can coexist; however, cardinality validation is **skipped** whenever the structural stage reports an error.

Currently, model-level warnings are generated for **empty models** and **isolated entities**. Parser-specific diagnostics, missing optional data and unmapped external objects should not automatically be interpreted as warnings produced by `Model.validate()`.

## Validation after loading a scenario

After creating a model through an importer or parser, call `model.validate()` and inspect the report before using the scenario. Parsing success does not imply metamodel validity.

The strict registration rules also mean that generic or unsupported classes created by legacy integrations may be rejected by `Model.add()`. Compatibility with individual parsers, including STIX, is separate from the structural guarantees documented here.

For complete, runnable demonstrations of the three outcomes, see:

- [Valid Model](../examples/13_valid_model/README.md) — no errors or warnings.
- [Warning Model](../examples/14_warning_model/README.md) — valid scenario with an isolated-entity warning.
- [Invalid Model](../examples/15_invalid_model/README.md) — reference and type errors deliberately introduced by bypassing preventive checks.

Related documentation: [Metamodel](metamodel.md), [I/O](io.md) and [Adapters](adapters.md).
