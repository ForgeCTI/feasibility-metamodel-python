# Valid Model

## Purpose

Demonstrate a minimal but fully valid model that satisfies all applicable relationship cardinalities using the complete validation system.

## Scenario

The scenario contains two threat actors sharing the same expertise.

**Entities:**
- 2 `ThreatActor`
- 1 `Expertise`

**Relationships:**
- 2 `hasExpertise`

Both threat actors are associated with the same expertise.

## Validation

The `hasExpertise` relationship defines the following cardinalities:

- `source_cardinality = "1..*"`: each Expertise must be associated with at least one ThreatActor.
- `target_cardinality = "1"`: each ThreatActor must be associated with exactly one Expertise.

The model satisfies these constraints without requiring additional entities or relationships.

Reference, type, and cardinality validation are executed through `Model.validate()` using the default Registry.

**Expected result:**

```text
Entities: 3
Relationships: 2
Valid: True
Errors: 0
Warnings: 0
```

## Run

From the repository root:

```bash
python examples/13_valid_model/main.py
```

## Notes

This example demonstrates a formally valid model without structural errors, cardinality violations, or isolated entities.

It is intended to illustrate the validation system, not to represent a complete cyber-attack feasibility analysis.