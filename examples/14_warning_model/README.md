# Warning Model

## Purpose

Demonstrate how the validation system handles isolated entities through warnings without automatically invalidating the model.

## Scenario

The scenario represents a threat actor associated with an adversary profile and a specific expertise. An unrelated application is intentionally included to demonstrate isolation detection.

**Entities:**
- 1 `ThreatActor`
- 1 `Expertise`
- 1 `Adversary`
- 1 `AdversaryType`
- 1 `Application`

**Relationships:**
- 1 `hasExpertise`
- 1 `relatedTo`
- 1 `hasAdversaryType`

The first four entities form a connected component that satisfies all applicable mandatory cardinalities.

The `Application` entity remains intentionally isolated.

## Validation

The complete validation process is executed through `Model.validate()` using the default Registry.

Reference and type validation succeed, and no mandatory cardinalities are violated.

However, the Cardinality Validator detects that `Standalone Application` does not participate in any relationship and generates a warning.

Since isolation alone does not constitute a validation error, the model remains formally valid.

**Expected result:**

```
Entities: 5
Relationships: 3
Valid: True
Errors: 0
Warnings: 1
Warning [cardinalityValidator]: Application 'Standalone Application' is isolated.
```

## Run

From the repository root:

```bash
python examples/14_warning_model/main.py
```

## Notes

This example demonstrates the distinction between validation errors and diagnostic warnings.

An isolated entity does not automatically invalidate a model, provided that all applicable mandatory cardinalities are satisfied.

It also illustrates that formal validity does not require every entity to belong to the same connected component.

The example is intended to demonstrate validation behavior, not to represent a complete cyber-attack feasibility analysis.