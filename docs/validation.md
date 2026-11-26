# Validation

Validation checks whether a scenario is consistent with the metamodel: relationships point to entities
of the model, connect the right entity types, respect the multiplicities of the paper, and satisfy a
few rules that multiplicities cannot express.

Many errors are caught earlier, when objects are created:

* entity attributes are validated by their setters (types, allowed values, ranges);
* a relationship checks the types of its endpoints when it is created;
* `Model.add` rejects relationships whose endpoints (or referenced entities, such as the privilege
  level of a grant) are not in the model, and duplicate relationships.

`model.validate()` then checks the complete scenario.

## Running validation

```python
from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn

model = Model()
organization = model.add(Organization(name="ExampleBank"))
model.add(operatesIn(organization, model.add(Sector(name="Finance"))))

report = model.validate()
print(report.is_valid)
for message in report.messages:
    print(f"[{message.severity}] {message.validator}: {message.message}")
```

The report exposes `is_valid` (no errors), `errors`, `warnings`, and `messages` (both). Each message is
a `ValidationMessage` with `validator`, `message`, and `severity` (`error` or `warning`). From the
command line:

```bash
metamodel validate scenario.yaml            # exit code 1 if not valid
metamodel validate scenario.yaml --json     # machine-readable report
metamodel validate scenario.yaml --strict   # warnings also make it fail
```

## Validators

| Validator | Checks | Severity |
|---|---|---|
| `referenceValidator` | relationship endpoints and entity-valued attributes belong to the model | error |
| `typeValidator` | relationship endpoints have the declared types (subclasses accepted) | error |
| `cardinalityValidator` | multiplicities at both ends of every relationship | error |
| | entities with no relationship at all | warning |
| `semanticValidator` | connection scopes and endpoints | error |
| | cycles in `followedBy` | error |
| | connections without scope, privilege levels without rank | warning |

Cardinality and semantic validation run only if the reference and type checks pass, since their results
would be meaningless otherwise. `validateReferences`, `validateTypes`, `validateCardinalities`, and
`validateSemantics` can also be called on their own from `metamodel.validation`.

## Multiplicities

Each relationship class declares the multiplicities at its source and target ends, as drawn in the
paper's figures; `metamodel schema <name>` and the [schema reference](schema.md) list them.

```text
Organization [0..*] --operatesIn--> [1..*] Sector
```

The target multiplicity constrains the outgoing relationships of each source entity (every
organization operates in at least one sector); the source multiplicity constrains the incoming
relationships of each target entity (a sector may have any number of organizations). Missing
relationships count as zero, so a mandatory relationship that is absent is reported:

```python
from metamodel.validation.cardinalityValidator import validateCardinalities

report = validateCardinalities(model)
print([m.message for m in report.errors if m.message.startswith("basedIn")])
# ["basedIn: Organization 'ExampleBank' has 0 target relationship(s); expected 1..*."]
```

Two refinements follow the metamodel:

* **Subclasses.** A multiplicity declared on a class applies to its subclasses: `Node --hostsResource-->
  Resource` is `1..*` at the node end, so every `Data`, `Code`, or `Asset` must be hosted by a node.
  Application and OS instances run by a node (`runsApp`, `runsOS`) count as hosted resources.
* **Associations with several target types.** One association of the paper may be implemented by
  several classes with the same label, e.g. `affects` from `SoftwareVulnerability` to `OS`
  (`affectsOS`) and to `Application` (`affectsApplication`), both `1..*`. Their target multiplicity is
  checked on the union: a software vulnerability must affect at least one OS or application. Likewise,
  an account must grant access to at least one node or resource.

## Semantic rules

* **Connection scope.** An `internal` connection has one source and one destination node (`isSource`,
  `isDestination`); an `inbound` connection only a destination (reachability from outside); an
  `outbound` connection only a source. A connection without scope produces a warning.
* **Threat-step ordering.** `followedBy` must be acyclic, so that steps can be evaluated in
  topological order (see Section 3.7 of the paper).
* **Privilege levels.** A level used by `grantsAccessTo` or `requiresPrivilegeLevel` should have a
  `rank`; otherwise grants and requirements cannot be compared (warning).

```python
from metamodel.infrastructure.entities.Connection import Connection
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.rels.isDestination import isDestination
from metamodel.infrastructure.rels.isSource import isSource
from metamodel.validation.semanticValidator import validateSemantics

gateway, server = model.add(Node(name="gateway")), model.add(Node(name="server"))
inbound = model.add(Connection(name="Inbound HTTPS", scope="inbound"))
model.add(isSource(gateway, inbound))       # an inbound connection has no source node
model.add(isDestination(server, inbound))
print(validateSemantics(model).errors[0].message)
```

## Validating parsed scenarios

Parsers raise `ParseError` for unknown types, unknown attributes, invalid values, or dangling
references, naming the entity involved; with `strict=False` they skip such items and return warnings
(`parseScenarioWithReport`). A parsed model should then be validated like any other:

<!-- no-test -->
```python
from metamodel.io import loadModel

model = loadModel("scenario.yaml")
report = model.validate()
```

For STIX bundles, also review the objects and relationships that were skipped or kept as generic STIX
entities:

<!-- no-test -->
```python
from metamodel.io.stixParser import loadStixBundleWithReport

result = loadStixBundleWithReport("bundle.json")
print(result.skipped_objects, result.skipped_relationships)
report = result.model.validate()
```

## Checklist

* `metamodel validate` reports no errors;
* warnings (isolated entities, connections without scope, levels without rank) have been reviewed;
* for scenarios derived from CTI, skipped STIX objects have been reviewed and assumptions are
  documented (e.g. in `case_studies/<case>/notes/`).
