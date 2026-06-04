# Installation

This page explains how to install the **CTI Feasibility Metamodel**, how to enable optional integrations, and how to set up a local development environment.

## Requirements

The package requires:

* Python 3.10 or later;
* `pip`;
* optionally, a virtual environment manager such as `venv`, `conda`, or `uv`.

Recommended Python versions:

```text
Python 3.10
Python 3.11
Python 3.12
```

## Basic installation

Install the base package with:

```bash
pip install cti-feasibility-metamodel
```

The base installation includes:

* the core model container;
* base entity and relationship classes;
* organization, infrastructure, and cyber-threat entities;
* organization, infrastructure, and cyber-threat relationships;
* validation utilities;
* basic JSON I/O utilities.

## Installation from GitHub

If the package has not yet been published on PyPI, install it directly from the GitHub repository:

```bash
pip install git+https://github.com/ForgeCTI/feasibility-metamodel-python.git
```

To install a specific branch:

```bash
pip install git+https://github.com/ForgeCTI/feasibility-metamodel-python.git@main
```

To install a specific tag or release:

```bash
pip install git+https://github.com/ForgeCTI/feasibility-metamodel-python.git@v0.1.0
```

## Development installation

For development, clone the repository and install the package in editable mode:

```bash
git clone https://github.com/ForgeCTI/feasibility-metamodel-python.git
cd feasibility-metamodel-python
pip install -e ".[all]"
```

Editable mode means that changes to the source files are immediately reflected in the installed package.

## Optional dependency groups

The package separates optional functionality into dependency groups. This keeps the base installation lightweight.

| Extra      | Purpose                                      |
| ---------- | -------------------------------------------- |
| `yaml`     | YAML scenario parsing and serialization.     |
| `networkx` | Conversion to NetworkX graph objects.        |
| `neo4j`    | Export to Neo4j graph databases.             |
| `docs`     | Build and preview the documentation locally. |
| `test`     | Run the test suite.                          |
| `all`      | Install all optional dependencies.           |

## Verify the installation

After installation, verify that the package can be imported:

```bash
python -c "import metamodel; print('CTI Feasibility Metamodel installed successfully')"
```

You can also instantiate a minimal model:

```bash
python - <<'PY'
from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization

model = Model()
organization = model.add_entity(Organization(name="ExampleBank"))

print(organization.type)
print(organization.name)
print(organization.id)
PY
```

Expected output:

```text
Organization
ExampleBank
<automatically-generated-id>
```

The exact identifier will be different every time because entity IDs are generated internally.

## Run an example (optional)

After installing the package in editable mode, run the first example:

```bash
python examples/01_organization_scenario/main.py
```

On Windows PowerShell:

```powershell
python examples\01_organization_scenario\main.py
```

If the example runs correctly, the package is installed and importable.

## Build the documentation locally (optional)

Install the documentation dependencies:

```bash
pip install -e ".[docs]"
```

Start the local documentation server:

```bash
mkdocs serve
```

Then open:

```text
http://127.0.0.1:8000/
```

To build the static site without serving it:

```bash
mkdocs build --strict
```

The generated site will be written to:

```text
site/
```

## Next steps

After installation, continue with:

* [Quickstart](quickstart.md) for a minimal end-to-end example;
* [Metamodel](metamodel.md) for the structure of the three sub-metamodels;
* [Taxonomies](taxonomies.md) for controlled vocabulary integration;
* [Validation](validation.md) for correctness checks;
* [I/O](io.md) for scenario loading and serialization;
* [Adapters](adapters.md) for NetworkX, Neo4j, and graph export.
