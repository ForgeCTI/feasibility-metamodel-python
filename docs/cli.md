# CLI

The **CTI Feasibility Metamodel** provides a minimal command-line interface for working with scenario files from a terminal.

The CLI is exposed through the `metamodel` command after the package is installed.

## Installation

Install the package in editable mode from the repository root:

```bash
pip install -e ".[all]"
```

Then verify that the command is available:

```bash
metamodel --help
```

If the command is not available, check that the active Python environment is the same environment where the package was installed.

## Entry point

The CLI entry point is configured in `pyproject.toml`:

```toml
[project.scripts]
metamodel = "metamodel.cli.main:main"
```

The implementation is located under:

```text
src/metamodel/cli/
├── __init__.py
├── main.py
├── validateCommand.py
├── inspectCommand.py
└── convertCommand.py
```

## Available commands

The current CLI implements three basic commands:

```text
metamodel validate <scenario-file>
metamodel inspect <scenario-file>
metamodel convert <scenario-file>
```

| Command    | Purpose                                               |
| ---------- | ----------------------------------------------------- |
| `validate` | Load a scenario file and run model validation.        |
| `inspect`  | Load a scenario file and print a basic model summary. |
| `convert`  | Load a scenario file and print the model as JSON.     |

The CLI is intentionally minimal at this stage. More advanced commands, such as direct Neo4j export, NetworkX export, STIX parsing, or selective inspection, may be added later.

## Supported input files

The CLI is intended to work with scenario files supported by the `io` module.

Typical inputs are:

```text
scenario.json
scenario.yaml
scenario.yml
```

YAML support requires the YAML optional dependency group:

```bash
pip install -e ".[yaml]"
```

or, for development with all extras:

```bash
pip install -e ".[all]"
```

## Scenario file structure

A minimal scenario file contains two top-level sections:

```yaml
entities:
  - id: org1
    type: Organization
    name: ExampleBank

  - id: sector1
    type: Sector
    name: Finance
    taxonomy_ref: sectors:finance

relationships:
  - id: rel1
    type: operatesIn
    source: org1
    target: sector1
```

The `id` values in the file are scenario-level identifiers. They are used to connect relationships to entities during parsing.

They are not the same as the internal automatically generated IDs assigned to Python objects.

## `validate`

The `validate` command loads a scenario and runs model validation.

```bash
metamodel validate scenario.yaml
```

Example output:

```text
Valid: True
```

If validation fails, the command prints validation errors.

Example:

```text
Valid: False
Errors:
- Relationship operatesIn references unknown target entity sector1.
- Cardinality violation: Organization must operate in at least one Sector.
```

Use this command before exporting or analyzing a scenario.

### Recommended use

```bash
metamodel validate case_studies/01_case_study/scenario.yaml
```

On Windows PowerShell:

```powershell
metamodel validate case_studies\01_case_study\scenario.yaml
```

## `inspect`

The `inspect` command loads a scenario and prints a basic summary.

```bash
metamodel inspect scenario.yaml
```

Example output:

```text
Entities: 2
Relationships: 1
```

This is useful for quickly checking whether a file was parsed and whether the expected number of objects was created.

### Recommended use

```bash
metamodel inspect examples/09_yaml_scenario_import/data/scenario.yaml
```

On Windows PowerShell:

```powershell
metamodel inspect examples\09_yaml_scenario_import\data\scenario.yaml
```

## `convert`

The `convert` command loads a scenario and prints a JSON representation of the resulting model.

```bash
metamodel convert scenario.yaml
```

Example output:

```json
{
  "entities": [
    {
      "id": "generated-internal-id",
      "type": "Organization",
      "name": "ExampleBank",
      "description": null,
      "source": null
    },
    {
      "id": "generated-internal-id",
      "type": "Sector",
      "name": "Finance",
      "description": null,
      "source": null,
      "taxonomy_ref": "sectors:finance"
    }
  ],
  "relationships": [
    {
      "id": "generated-relationship-id",
      "type": "operatesIn",
      "source": "generated-organization-id",
      "target": "generated-sector-id"
    }
  ]
}
```

To save the output to a file:

```bash
metamodel convert scenario.yaml > scenario.json
```

On Windows PowerShell:

```powershell
metamodel convert scenario.yaml | Out-File -Encoding utf8 scenario.json
```

## Example workflow

A common CLI workflow is:

```bash
metamodel inspect case_studies/01_case_study/scenario.yaml
metamodel validate case_studies/01_case_study/scenario.yaml
metamodel convert case_studies/01_case_study/scenario.yaml > case_studies/01_case_study/output/scenario.json
```

This workflow:

1. checks that the scenario can be loaded;
2. validates the model;
3. writes a JSON representation to the case-study output folder.

## Using the CLI in CI

The CLI can be used in GitHub Actions or other CI systems.

Example step:

```yaml
- name: Validate case studies
  run: |
    metamodel validate case_studies/01_case_study/scenario.yaml
    metamodel validate case_studies/02_case_study/scenario.yaml
    metamodel validate case_studies/03_case_study/scenario.yaml
    metamodel validate case_studies/04_case_study/scenario.yaml
    metamodel validate case_studies/05_case_study/scenario.yaml
```

This makes validation part of the repository workflow.

## Current limitations

The current CLI is intentionally small.

The following commands are not yet implemented unless added later:

```bash
metamodel export scenario.yaml --to networkx
metamodel export scenario.yaml --to neo4j
metamodel parse-stix bundle.json
metamodel inspect scenario.yaml --entities
metamodel inspect scenario.yaml --relationships
metamodel validate scenario.yaml --strict
```

For these workflows, use the Python API directly.

For example, to parse STIX:

```python
from metamodel.io.stixParser import loadStixBundleWithReport

result = loadStixBundleWithReport("bundle.json")
model = result.model
```

To export to NetworkX:

```python
from metamodel.adapters.networkxAdapter import toNetworkx

graph = toNetworkx(model)
```

To export to Neo4j:

```python
from metamodel.adapters.neo4jAdapter import exportToNeo4j

exportToNeo4j(
    model,
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
)
```

## Common issues

### `metamodel` command not found

The package may not be installed in the active environment.

Run:

```bash
pip install -e ".[all]"
```

Then try:

```bash
metamodel --help
```

If it still fails, run the CLI as a Python module if supported by your environment:

```bash
python -m metamodel.cli.main --help
```

### `ModuleNotFoundError: No module named 'metamodel'`

The active Python environment does not contain the package.

Check the Python executable:

```bash
python -c "import sys; print(sys.executable)"
```

Then reinstall:

```bash
pip install -e ".[all]"
```

### YAML file cannot be loaded

Install YAML support:

```bash
pip install -e ".[yaml]"
```

or:

```bash
pip install -e ".[all]"
```

### Output contains generated IDs

This is expected.

Scenario file IDs are used only during parsing. Entity and relationship objects receive internal automatically generated IDs.

## Recommended practice

Use the CLI for lightweight checks:

```bash
metamodel inspect scenario.yaml
metamodel validate scenario.yaml
```

Use the Python API for richer workflows:

* STIX parsing;
* custom mapper registration;
* NetworkX analysis;
* Neo4j export;
* case-study-specific automation;
* advanced validation policies.

## Next steps

Continue with:

* [I/O](io.md) for scenario parsing and serialization;
* [Validation](validation.md) for model correctness checks;
* [Adapters](adapters.md) for NetworkX, Neo4j, and graph export;
* [Examples](examples/organizationScenario.md) for runnable examples.
