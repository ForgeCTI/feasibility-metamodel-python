# CTI Feasibility Metamodel

A Python package for modelling interactions among organization, infrastructure, and cyber-threat concepts.

The package follows these conventions:

- one file for each entity;
- one file for each relationship;
- entity file names and class names match the exact metamodel entity names;
- relationship names are concise lower-camel-case names;
- entity identifiers are internal and automatically generated;
- relationships do not carry traceability metadata;
- optional taxonomies can be used for controlled vocabularies such as attack tools, TTPs, sectors, platforms, and vulnerability classes.

## Installation

```bash
pip install cti-feasibility-metamodel
```

For optional integrations:

```bash
pip install cti-feasibility-metamodel[networkx]
pip install cti-feasibility-metamodel[neo4j]
pip install cti-feasibility-metamodel[yaml]
```

## Minimal example

```python
from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn

model = Model()
org = model.add_entity(Organization(name="ExampleBank"))
sector = model.add_entity(Sector(name="Finance", taxonomy_ref="sectors:finance"))
model.add_relationship(operatesIn(org, sector))

report = model.validate()
print(report.is_valid)
```
