# cti-metamodel

Python package to be used in the framework. Provides access to the metamodel's entities and relationships and enforce maintainability of the codebase.

## Package Organization

The package is organized into three main parts:
- `core`: it contains the abstract classes to be used to define new entities and relationships
- `metamodel`: it contains the entities and relationships organized into the three sub-metamodels: `cyber_threat`, `infrastructure`, and `organization`. Each sub-metamodel is organized into `entities` and `rels`.
- `taxonomies`: it contains the defined taxonomies (e.g., the CIA triad)

## How to use?

In the file `requirements.txt` add:

`cti-metamodel @ git+https://github.com/ForgeCTI/cti-metamodel.git@<version>`
