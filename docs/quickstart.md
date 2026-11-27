# Quickstart

This page introduces the basic workflow of the **CTI Feasibility Metamodel** through a small end-to-end scenario.

The goal is to show how to:

1. create a model;
2. instantiate entities;
3. connect entities with relationships;
4. validate the model;
5. inspect or export the resulting scenario.

## Scenario

In this quickstart, we model a simple CTI feasibility scenario:

```text
An organization operates in the finance sector.

The organization manages an infrastructure composed of a public-facing web server.
The web server exposes an HTTPS port and hosts a web application resource.

A threat actor initiates a threat composed of a threat step.
The threat step exploits a vulnerability and targets the web application resource.
```

This is intentionally small, but it already touches the three sub-metamodels:

| Sub-metamodel    | Example concepts                                              |
| ---------------- | ------------------------------------------------------------- |
| `organization`   | `Organization`, `Sector`                                      |
| `infrastructure` | `Infrastructure`, `Node`, `Port`, `Resource`                  |
| `cyberThreat`    | `ThreatActor`, `Threat`, `ThreatStep`, `Vulnerability`, `TTP` |

## Create a Python file

Create a file named:

```text
quickstart.py
```

Then add the following code.

## Complete example

```python
from metamodel.core.Model import Model

from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn

from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.NodeType import NodeType
from metamodel.infrastructure.entities.Port import Port
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.infrastructure.rels.manages import manages
from metamodel.infrastructure.rels.madeBy import madeBy
from metamodel.infrastructure.rels.hasNodeType import hasNodeType
from metamodel.infrastructure.rels.exposesPort import exposesPort
from metamodel.infrastructure.rels.hostsResource import hostsResource

from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.Vulnerability import Vulnerability
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.rels.initiates import initiates
from metamodel.cyberThreat.rels.startsWith import startsWith
from metamodel.cyberThreat.rels.exploits import exploits
from metamodel.cyberThreat.rels.targetsResource import targetsResource
from metamodel.cyberThreat.rels.implementsTTP import implementsTTP


def build_model() -> Model:
    model = Model()

    # -------------------------------------------------------------------------
    # Organization sub-metamodel
    # -------------------------------------------------------------------------

    organization = model.add(
        Organization(
            name="ExampleBank",
            description="Example financial organization.",
            organization_size="enterprise",
            criticality="critical",
            source="Quickstart scenario",
        )
    )

    sector = model.add(
        Sector(
            name="Finance",
        )
    )

    model.add(
        operatesIn(
            source_entity=organization,
            target_entity=sector,
        )
    )

    # -------------------------------------------------------------------------
    # Infrastructure sub-metamodel
    # -------------------------------------------------------------------------

    infrastructure = model.add(
        Infrastructure(
            name="ExampleBank production infrastructure",
            description="Simplified production infrastructure.",
            environment_type="production",
            scope="internet-facing services",
            source="Quickstart scenario",
        )
    )

    web_server_type = model.add(
        NodeType(
            name="Web server",
            category="server",
        )
    )

    web_server = model.add(
        Node(
            name="public-web-01",
            hostname="public-web-01.examplebank.test",
            ip_addresses=["203.0.113.10"],
            source="Quickstart scenario",
        )
    )

    https_port = model.add(
        Port(
            name="HTTPS",
            number=443,
            protocol="tcp",
            service_name="https",
            state="open",
        )
    )

    web_application = model.add(
        Resource(
            name="Customer web portal",
            description="Public-facing customer web application.",
            source="Quickstart scenario",
        )
    )

    model.add(
        manages(
            source_entity=organization,
            target_entity=infrastructure,
        )
    )

    model.add(
        madeBy(
            source_entity=infrastructure,
            target_entity=web_server,
        )
    )

    model.add(
        hasNodeType(
            source_entity=web_server,
            target_entity=web_server_type,
        )
    )

    model.add(
        exposesPort(
            source_entity=web_server,
            target_entity=https_port,
        )
    )

    model.add(
        hostsResource(
            source_entity=web_server,
            target_entity=web_application,
        )
    )

    # -------------------------------------------------------------------------
    # Cyber-threat sub-metamodel
    # -------------------------------------------------------------------------

    threat_actor = model.add(
        ThreatActor(
            name="Example financially motivated actor",
            description="Fictitious actor used in the quickstart.",
            aliases=["ExampleActor"],
            motivation="financial_gain",
            sophistication="medium",
            source="Quickstart scenario",
        )
    )

    threat = model.add(
        Threat(
            name="Web portal compromise",
            description="Threat scenario targeting the public web portal.",
            objective="Gain unauthorized access to customer data.",
            source="Quickstart scenario",
        )
    )

    threat_step = model.add(
        ThreatStep(
            name="Exploit public-facing web application",
            description="The attacker exploits a web application vulnerability.",
            phase="initial_access",
            objective="Obtain initial access through the web portal.",
            preconditions=[
                "The web application is reachable from the Internet.",
                "The application contains an exploitable vulnerability.",
            ],
            postconditions=[
                "The attacker gains unauthorized access to the application.",
            ],
            source="Quickstart scenario",
        )
    )

    ttp = model.add(
        TTP(
            name="Exploit Public-Facing Application",
            description="Adversaries exploit a public-facing application.",
            external_id="T1190",
            tactic="initial_access",
            technique="Exploit Public-Facing Application",
            source="MITRE ATT&CK",
        )
    )

    vulnerability = model.add(
        Vulnerability(
            name="Example web application vulnerability",
            description="Fictitious vulnerability used in the quickstart.",
            external_id="CVE-2099-0001",
            severity="high",
            cvss_score=8.5,
            source="Quickstart scenario",
        )
    )

    model.add(
        initiates(
            source_entity=threat_actor,
            target_entity=threat,
        )
    )

    model.add(
        startsWith(
            source_entity=threat,
            target_entity=threat_step,
        )
    )

    model.add(
        implementsTTP(
            source_entity=threat_step,
            target_entity=ttp,
        )
    )

    model.add(
        exploits(
            source_entity=threat_step,
            target_entity=vulnerability,
        )
    )

    model.add(
        targetsResource(
            source_entity=threat_step,
            target_entity=web_application,
        )
    )

    return model


def main() -> None:
    model = build_model()

    print("CTI Feasibility Metamodel quickstart")
    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")

    report = model.validate()

    print(f"Valid: {report.is_valid}")

    if report.errors:
        print("Validation errors:")
        for error in report.errors:
            print(f"- {error.message}")

    if report.warnings:
        print("Validation warnings:")
        for warning in report.warnings:
            print(f"- {warning.message}")

    print("\nEntities:")
    for entity in model.entities:
        print(f"- {entity.type}: {entity.name}")

    print("\nRelationships:")
    for relationship in model.relationships:
        print(
            f"- {relationship.type}: "
            f"{relationship.source_entity.name} -> {relationship.target_entity.name}"
        )


if __name__ == "__main__":
    main()
```

## Run the quickstart

Run the file:

```bash
python quickstart.py
```

You should see output similar to:

```text
CTI Feasibility Metamodel quickstart
Entities: 12
Relationships: 11
Valid: False
Validation errors:
- hasBusinessRequirement: Organization 'ExampleBank' has 0 target relationship(s); expected 1..*.
- runsOS: Node 'public-web-01' has 0 target relationship(s); expected 1.
- threatPartOf: Threat 'Web portal compromise' has 0 target relationship(s); expected 1.
- hasExpertise: ThreatActor 'Example financially motivated actor' has 0 target relationship(s); expected 1.
- exploitsVulnerability: Vulnerability 'Example web application vulnerability' has 0 source relationship(s); expected 1..*.
- compromises: ThreatStep 'Exploit public-facing web application' has 0 target relationship(s); expected 1.
- listensOn: Port 'HTTPS' has 0 source relationship(s); expected 1.
- usedBy: Infrastructure 'ExampleBank production infrastructure' has 0 target relationship(s); expected 1..*.
- violates: TTP 'Exploit Public-Facing Application' has 0 target relationship(s); expected 1..*.
- hasDestinationPort: Port 'HTTPS' has 0 source relationship(s); expected 1..*.

Entities:
- Organization: ExampleBank
- Sector: Finance
- Infrastructure: ExampleBank production infrastructure
- NodeType: Web server
- Node: public-web-01
- Port: HTTPS
- Resource: Customer web portal
- ThreatActor: Example financially motivated actor
- Threat: Web portal compromise
- ThreatStep: Exploit public-facing web application
- TTP: Exploit Public-Facing Application
- Vulnerability: Example web application vulnerability

Relationships:
- operatesIn: ExampleBank -> Finance
- manages: ExampleBank -> ExampleBank production infrastructure
- madeBy: ExampleBank production infrastructure -> public-web-01
- hasNodeType: public-web-01 -> Web server
- exposesPort: public-web-01 -> HTTPS
- hostsResource: public-web-01 -> Customer web portal
- initiates: Example financially motivated actor -> Web portal compromise
- startsWith: Web portal compromise -> Exploit public-facing web application
- implementsTTP: Exploit public-facing web application -> Exploit Public-Facing Application
- exploits: Exploit public-facing web application -> Example web application vulnerability
- targetsResource: Exploit public-facing web application -> Customer web portal
```

The model is intentionally partial: it can be constructed successfully, but formal validation reports errors because some mandatory relationships are missing. The cardinality validator checks minimum cardinalities even when no relationship of a given type is present. Warnings alone do not make a model invalid. See [Validation](validation.md) for details.

The exact output may vary depending on the validation rules and entity attributes currently implemented.

## Understanding the example

The quickstart creates a small model:

```text
Organization → Sector
Organization → Infrastructure
Infrastructure → Node
Node → NodeType
Node → Port
Node → Resource

ThreatActor → Threat
Threat → ThreatStep
ThreatStep → TTP
ThreatStep → Vulnerability
ThreatStep → Resource
```

This is the core idea of the package: CTI feasibility is modelled by connecting threat knowledge to concrete organizational and infrastructure context.

## Internal identifiers

Every entity and relationship receives an internal automatically generated identifier.

You do not provide the internal ID manually:

```python
organization = Organization(name="ExampleBank")
print(organization.id)
```

The ID is generated when the object is created. It is used internally by the model, serializers, and graph adapters.

## Attribute validation

Entities use normal Python attributes with getters and setters.

For example:

```python
organization = Organization(name="ExampleBank")
organization.criticality = "critical"
```

Invalid values raise exceptions:

```python
organization.criticality = 123
```

This raises a `TypeError` because `criticality` must be a string or `None`.

Relationships also check source and target types. For example, `operatesIn` must connect:

```text
Organization → Sector
```

It should not connect:

```text
Node → Sector
```

## Exporting to NetworkX

If the NetworkX extra is installed:

```bash
pip install -e ".[networkx]"
```

you can convert the model to a graph:

```python
from metamodel.adapters.networkxAdapter import toNetworkx

graph = toNetworkx(model)

print(graph.number_of_nodes())
print(graph.number_of_edges())
```

This is useful for graph traversal, path analysis, centrality measures, and visualization.

## Loading from files

The package also supports scenario loading through the `io` module.

For example, a YAML or JSON scenario can be parsed into a `Model` object, depending on the installed optional dependencies and implemented parsers.

A minimal scenario file may look like this:

```yaml
entities:
  - id: org1
    type: Organization
    name: ExampleBank

  - id: sector1
    type: Sector
    name: Finance

relationships:
  - id: rel1
    type: operatesIn
    source: org1
    target: sector1
```

File-based scenarios are useful for repeatable case studies and automated validation.

## Next steps

After this quickstart, continue with:

* [Metamodel](metamodel.md) for the full conceptual structure;
* [Validation](validation.md) for model correctness checks;
* [I/O](io.md) for file-based scenarios and parsers;
* [Adapters](adapters.md) for NetworkX, Neo4j, and other integrations;
* [Examples](examples/organizationScenario.md) for runnable examples.
