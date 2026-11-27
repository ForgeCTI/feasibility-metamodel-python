# CTI Feasibility Metamodel

A Python package for representing and validating scenarios involving organizations, infrastructures and cyber threats.

The metamodel currently defines **39 entity types** and **62 relationship types** across three domains: `organization`, `infrastructure`, and `cyberThreat`.

The package follows these conventions:

- One Python class and file per entity or relationship type.
- Entity class and file names match the corresponding metamodel names.
- Relationship class names use lower camel case.
- Entity and relationship identifiers are generated internally.
- Relationship types declare their allowed source and target entity classes and, where specified, cardinality constraints.

## Installation

Python **3.10 or later** is required. From the repository root, install the package in editable mode:

```bash
pip install -e .
```

Optional integrations can be installed as needed:

```bash
pip install -e ".[yaml,networkx,neo4j]"
```

## Minimal example

```python
from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Expertise import Expertise
from metamodel.cyberThreat.rels.hasExpertise import hasExpertise

model = Model()
actor = model.add(ThreatActor(name="Example Actor"))
expertise = model.add(Expertise(name="Social Engineering"))
model.add(hasExpertise(actor, expertise))

report = model.validate()
print("Valid:", report.is_valid)
print("Errors:", len(report.errors))
print("Warnings:", len(report.warnings))
```

Expected output:

```text
Valid: True
Errors: 0
Warnings: 0
```

## Model validation

`Model.add()` prevents the insertion of unregistered entity and relationship classes, relationships with endpoints outside the model, and duplicate relationships.

`Model.validate()` produces a `ValidationReport` in two stages:

1. **Structural checks:** reference integrity, type registration and compatibility, and relationship uniqueness.
2. **Cardinality checks:** relationship multiplicities and warnings for isolated entities. This stage runs only if no structural errors were found.

Errors invalidate the model; warnings alone do not. Validation establishes consistency with the metamodel, not the feasibility of a cyber attack.

See [Validation](docs/validation.md) for details.

## Extending the metamodel

To introduce a new entity or relationship type:

1. Define a concrete class inheriting from `BaseEntity` or `BaseRelationship`, following the existing domain package conventions. Relationship classes must declare compatible `source_type` and `target_type` and their cardinalities where applicable.
2. Add the class to `ENTITY_IMPORTS` or `RELATIONSHIP_IMPORTS` in `src/metamodel/registry_data.py`. Add a relationship alias only if alias-based resolution is needed.
3. Add or update tests to verify construction, model insertion, and validation.

`Registry.load_default()` loads the classes listed in `registry_data.py`. Merely creating a new Python class is not sufficient: unregistered classes are rejected by `Model.add()` and flagged by the Type Validator.

## UML diagram generation

The repository includes a script for automatically generating UML diagrams from the Python implementation of the metamodel.

Run from the repository root:

```bash
python scripts/generate_uml.py --src src --reference docs/diagrams/metamodel_v2.drawio --output-dir docs/diagrams
```

The script generates both the entity structure and the complete class diagram in Draw.io and SVG formats.

When extending the metamodel, keep `metamodel_v2.drawio` consistent with the Python implementation. New or renamed entities must have corresponding class positions in the reference diagram.

See [UML diagram generation](docs/metamodel.md#uml-diagram-generation) for further details and maintenance guidelines.
