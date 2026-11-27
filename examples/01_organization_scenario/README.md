# Organization scenario

## Purpose

Instantiate a minimal organization-level scenario with an organization, a sector, an asset, and security requirements.

## Run

From the repository root:

```bash
python examples/01_organization_scenario/main.py
```

## Notes

This example focuses on the construction of a partial organization-level scenario and does not aim to satisfy every mandatory relationship cardinality defined by the complete metamodel.

Consequently, `Model.validate()` reports cardinality violations and the model is considered formally invalid (`Valid: False`).

This behavior is expected under the current strict validation rules and does not prevent the example from demonstrating entity and relationship instantiation.

For examples specifically designed to demonstrate validation outcomes, see `13_valid_model`, `14_warning_model`, and `15_invalid_model`.
