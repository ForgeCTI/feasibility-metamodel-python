# Quickstart

This page builds a small scenario in Python, validates it, saves it in several formats, and exports it
to graph tools. It is a reduced version of the motivating example of the paper (credential phishing
against a mailbox); the full version is `examples/13_motivating_example/data/scenario.yaml`.

Install the package with the optional dependencies used below:

```bash
pip install -e ".[yaml,networkx]"
```

## Scenario

A defence organization runs a mail server reachable from the Internet over HTTPS. An employee has a
cloud mailbox account with standard privileges on the mailbox emails, whose confidentiality is a
business requirement. A threat actor's campaign phishes the employee (TS1), steals the session
cookie (TS2), and collects the emails (TS3).

## Organization and infrastructure

```python
from metamodel.core.Model import Model

from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.HomeCountry import HomeCountry
from metamodel.organization.entities.BusinessRequirement import BusinessRequirement
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement
from metamodel.organization.entities.Asset import Asset
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.organization.rels.basedIn import basedIn
from metamodel.organization.rels.hasBusinessRequirement import hasBusinessRequirement
from metamodel.organization.rels.drivesSecurityRequirement import drivesSecurityRequirement
from metamodel.organization.rels.hasSecurityRequirement import hasSecurityRequirement
from metamodel.organization.rels.implementsRequirement import implementsRequirement

from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.NodeType import NodeType
from metamodel.infrastructure.entities.Port import Port
from metamodel.infrastructure.entities.Connection import Connection
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.UserType import UserType
from metamodel.infrastructure.entities.Account import Account
from metamodel.infrastructure.entities.PrivilegeLevel import PrivilegeLevel
from metamodel.infrastructure.rels.manages import manages
from metamodel.infrastructure.rels.madeBy import madeBy
from metamodel.infrastructure.rels.usedBy import usedBy
from metamodel.infrastructure.rels.hasNodeType import hasNodeType
from metamodel.infrastructure.rels.hostsResource import hostsResource
from metamodel.infrastructure.rels.exposesPort import exposesPort
from metamodel.infrastructure.rels.isDestination import isDestination
from metamodel.infrastructure.rels.hasDestinationPort import hasDestinationPort
from metamodel.infrastructure.rels.hasUserType import hasUserType
from metamodel.infrastructure.rels.hasAccount import hasAccount
from metamodel.infrastructure.rels.grantsAccessToResource import grantsAccessToResource

model = Model()
model.metadata["name"] = "Quickstart scenario"

# Organization
org = model.add(Organization(name="Defence organization"))
model.add(operatesIn(org, model.add(Sector(name="Defence"))))
model.add(basedIn(org, model.add(HomeCountry(name="United Kingdom"))))
requirement = model.add(BusinessRequirement(name="Confidentiality of mission emails"))
model.add(hasBusinessRequirement(org, requirement))

# The emails are an Asset, i.e. a Resource with an asset security requirement.
emails = model.add(Asset(name="Mailbox emails"))
asr = model.add(AssetSecurityRequirement(name="Confidentiality of mailbox emails"))
model.add(drivesSecurityRequirement(requirement, asr))
model.add(hasSecurityRequirement(emails, asr))
model.add(implementsRequirement(asr, model.add(SecurityRequirement(name="Confidentiality"))))

# Infrastructure: a mail server reachable from the Internet on 443/tcp.
infra = model.add(Infrastructure(name="Corporate infrastructure"))
model.add(manages(org, infra))
mx = model.add(Node(name="Mail server", hostname="mx1"))
model.add(madeBy(infra, mx))
model.add(hasNodeType(mx, model.add(NodeType(name="Server"))))
model.add(hostsResource(mx, emails))
https = model.add(Port(name="HTTPS", number=443, protocol="tcp"))
model.add(exposesPort(mx, https))
inbound = model.add(Connection(name="Inbound HTTPS", scope="inbound"))  # destination only
model.add(isDestination(mx, inbound))
model.add(hasDestinationPort(inbound, https))

# A user, her account, and the privilege level the account grants on the emails.
victim = model.add(User(name="Victim user"))
model.add(usedBy(infra, victim))
model.add(hasUserType(victim, model.add(UserType(name="Employee"))))
account = model.add(Account(name="Mailbox account", kind="cloud"))
model.add(hasAccount(victim, account))
standard = model.add(PrivilegeLevel(name="Standard user", rank=1))
model.add(grantsAccessToResource(account, emails, privilege_level=standard))
```

Relationship classes check their endpoint types when they are created, so `operatesIn(mx, org)` raises
a `TypeError`. `grantsAccessTo` carries the privilege level of the grant (the association class
`PrivilegeLevel` of the metamodel); the level must be added to the model before the grant.

## Cyber threat

```python
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.entities.HumanVulnerability import HumanVulnerability
from metamodel.cyberThreat.rels.initiates import initiates
from metamodel.cyberThreat.rels.startsWith import startsWith
from metamodel.cyberThreat.rels.followedBy import followedBy
from metamodel.cyberThreat.rels.implementsTTP import implementsTTP
from metamodel.cyberThreat.rels.affectsUser import affectsUser
from metamodel.cyberThreat.rels.exploits import exploits
from metamodel.cyberThreat.rels.targetsResource import targetsResource
from metamodel.cyberThreat.rels.compromises import compromises

actor = model.add(ThreatActor(name="Star Blizzard"))
threat = model.add(Threat(name="Credential phishing and mailbox exfiltration"))
model.add(initiates(actor, threat))

steps = []
for name, technique, technique_name in [
    ("TS1: phishing link", "T1566.001", "Spearphishing Attachment"),
    ("TS2: steal session cookie", "T1539", "Steal Web Session Cookie"),
    ("TS3: collect emails", "T1114.002", "Remote Email Collection"),
]:
    step = model.add(ThreatStep(name=name))            # join="AND" by default
    model.add(implementsTTP(step, model.add(TTP(name=technique_name, external_id=technique))))
    if steps:
        model.add(followedBy(steps[-1], step))
    steps.append(step)
model.add(startsWith(threat, steps[0]))

# A-posteriori knowledge: an observed weakness and the edges inferred by the evaluation.
susceptibility = model.add(HumanVulnerability(name="Phishing susceptibility"))
model.add(affectsUser(susceptibility, victim))
model.add(exploits(steps[0], susceptibility))
model.add(targetsResource(steps[2], emails))
model.add(compromises(steps[2], asr))
```

## Validate

```python
report = model.validate()
for message in report.messages:
    print(f"[{message.severity}] {message.validator}: {message.message}")
print("Valid:", report.is_valid)
assert report.is_valid
```

Validation checks references, endpoint types, multiplicities, and the rules described in
[Validation](validation.md). Each entity also knows its knowledge class:

```python
print(account.knowledge_class, standard.knowledge_class, steps[0].knowledge_class)
# system concept posteriori
```

## Save and load

```python
import tempfile
from pathlib import Path

from metamodel.io import loadModel, saveModel

folder = Path(tempfile.mkdtemp())
saveModel(model, folder / "scenario.yaml")
saveModel(model, folder / "scenario.json")
saveModel(model, folder / "scenario_csv", "csv")     # entities.csv + relationships.csv

loaded = loadModel(folder / "scenario.yaml")
assert loaded.get_entity(account.id).name == "Mailbox account"   # ids are preserved
assert len(loaded.relationships) == len(model.relationships)
```

In scenario files, relationships can be written with the metamodel label instead of the class name:

```yaml
relationships:
  - {type: grantsAccessTo, source: mailbox-account, target: emails, privilege_level: standard}
```

See [I/O](io.md) for the format.

## Export to graph tools

```python
from metamodel.adapters import toNetworkx, toCypherScript

graph = toNetworkx(model)
resources = [d["name"] for _, d in graph.nodes(data=True) if "Resource" in d["labels"]]
print(resources)                                    # ['Mailbox emails']

cypher = toCypherScript(model)                      # load with cypher-shell or Neo4j Browser
print(cypher.splitlines()[1])
```

With a running Neo4j server, `exportToNeo4j(model, uri, user, password)` writes the model directly;
see [Adapters](adapters.md).

## Command line

The same steps are available from the terminal:

```bash
metamodel validate examples/13_motivating_example/data/scenario.yaml
metamodel inspect examples/13_motivating_example/data/scenario.yaml
metamodel convert examples/13_motivating_example/data/scenario.yaml -o scenario.graphml
metamodel schema grantsAccessTo
```

See [CLI](cli.md).

## Next steps

* [Metamodel](metamodel.md) and the [schema reference](schema.md) for every entity, relationship, and multiplicity;
* [Validation](validation.md) for what is checked;
* `examples/13_motivating_example` for the full scenario and its variant with phishing-resistant MFA.
