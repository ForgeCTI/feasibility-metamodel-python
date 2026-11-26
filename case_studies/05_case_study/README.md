# Case Study 05 - Coordinated Cyber-Espionage Campaign

This folder contains Case Study 05 for the CTI Feasibility Metamodel.

## Purpose

This case study models a fictional cyber-espionage campaign targeting the research document management environment of **Asterion Research Institute**, an Italian scientific research organization.

The scenario focuses on threat actor alias correlation, campaign targeting, virtualized infrastructure, legitimate user access, the exploitation of an unclassified vulnerability, and multistage attack tool deployment.

The main objective is to demonstrate how entities and relationships from the **Organization**, **Infrastructure**, and **CyberThreat** submodels can be instantiated and combined to represent a coherent cyberattack scenario.

In particular, this case study illustrates how a single threat can be attributed to an actor with an alternative CTI identity, how the victim's geographic and institutional context can be represented, and how two attack tools can participate in successive steps of an intrusion targeting confidential research documents.

## Scenario

Asterion Research Institute is a fictional Italian research organization involved in international scientific programs. In this scenario, Italy is represented as a member of the fictional European Research Cooperation Council (ERCC).

The institute manages a production infrastructure consisting of a physical hypervisor and a virtual machine dedicated to research document management. The virtual machine runs the research portal, which implements a Python document viewer. A legitimate researcher account is authorized to access the virtual machine, launch the viewer, and consult confidential research results in PDF format.

A fictional threat actor, **Silent Horizon Group**, also known as **Ghost Meridian**, initiates a single threat named Research Portal Espionage, which belongs to the European Research Espionage Campaign. The campaign focuses on Italy and targets both the scientific research sector and the ERCC.

The attack consists of two main steps:

1. **Research Portal Compromise:** the attacker exploits an unclassified access weakness in the research portal, establishes unauthorized access, and deploys the first-stage tool, Horizon Loader. The loader deploys a second tool, Meridian Collector, on the same virtual machine.
2. **Research Document Collection:** the attacker abuses an accessible legitimate research session and employs Meridian Collector to collect confidential research documents.

The weakness is instantiated directly as a `Vulnerability` because the available fictional evidence is insufficient to classify it as a specific vulnerability subtype. Its severity is assessed as High in the scenario, but no CVSS score is assigned.

All organizations (except the real geographic reference to Italy), systems, vulnerabilities, adversaries, tools, and incident details are fictional and intended for demonstration purposes. The ERCC membership is a scenario assumption. Example addresses and domains are not operational targets, and tool hashes are derived from synthetic labels rather than real malware samples.

## Model Implementation

The implementation contains **23 entities** and **31 relationships**, distributed across the three submodels.

### Entities

| Submodel | Entity | Instance |
|---|---|---|
| Organization | Organization | Asterion Research Institute |
| Organization | Sector | Scientific Research and Development |
| Organization | HomeCountry | Italy |
| Organization | InternationalBody | European Research Cooperation Council |
| Infrastructure | Infrastructure | Asterion Research IT Infrastructure |
| Infrastructure | Node | Asterion Physical Hypervisor |
| Infrastructure | Node | Research Document VM |
| Infrastructure | User | Asterion Researcher Account |
| Infrastructure | Application | Asterion Research Document Portal |
| Infrastructure | ApplicationInstance | Research Portal Production Instance |
| Infrastructure | Code | Research Document Viewer |
| Infrastructure | Information | Confidential Research Results |
| CyberThreat | ThreatActor | Silent Horizon Group |
| CyberThreat | ThreatActor | Ghost Meridian |
| CyberThreat | Campaign | European Research Espionage Campaign |
| CyberThreat | Threat | Research Portal Espionage |
| CyberThreat | ThreatStep | Research Portal Compromise |
| CyberThreat | ThreatStep | Research Document Collection |
| CyberThreat | Vulnerability | Unclassified Research Portal Weakness |
| CyberThreat | AttackTool | Horizon Loader |
| CyberThreat | AttackTool | Meridian Collector |
| CyberThreat | AttackToolInstance | Horizon Loader VM Instance |
| CyberThreat | AttackToolInstance | Meridian Collector VM Instance |

### Relationships

| Relationship | Source | Target |
|---|---|---|
| `operatesIn` | Asterion Research Institute | Scientific Research and Development |
| `basedIn` | Asterion Research Institute | Italy |
| `countryPartOf` | Italy | European Research Cooperation Council |
| `manages` | Asterion Research Institute | Asterion Research IT Infrastructure |
| `madeBy` | Asterion Research IT Infrastructure | Asterion Physical Hypervisor |
| `madeBy` | Asterion Research IT Infrastructure | Research Document VM |
| `runs` | Asterion Physical Hypervisor | Research Document VM |
| `usedBy` | Asterion Research IT Infrastructure | Asterion Researcher Account |
| `hasAccessTo` | Asterion Researcher Account | Research Document VM |
| `runsApp` | Research Document VM | Research Portal Production Instance |
| `applicationInstanceOf` | Research Portal Production Instance | Asterion Research Document Portal |
| `applicationImplementsCode` | Research Portal Production Instance | Research Document Viewer |
| `launches` | Asterion Researcher Account | Research Document Viewer |
| `accessesInformation` | Research Document Viewer | Confidential Research Results |
| `userAccessesInformation` | Asterion Researcher Account | Confidential Research Results |
| `aliasOf` | Ghost Meridian | Silent Horizon Group |
| `initiates` | Silent Horizon Group | Research Portal Espionage |
| `threatPartOf` | Research Portal Espionage | European Research Espionage Campaign |
| `focusesOnCountry` | European Research Espionage Campaign | Italy |
| `targetsInternationalBody` | European Research Espionage Campaign | European Research Cooperation Council |
| `targetsSector` | European Research Espionage Campaign | Scientific Research and Development |
| `startsWith` | Research Portal Espionage | Research Portal Compromise |
| `followedBy` | Research Portal Compromise | Research Document Collection |
| `exploits` | Research Portal Compromise | Unclassified Research Portal Weakness |
| `employsTool` | Research Portal Compromise | Horizon Loader VM Instance |
| `employsTool` | Research Document Collection | Meridian Collector VM Instance |
| `deploysTool` | Horizon Loader VM Instance | Meridian Collector VM Instance |
| `toolInstanceOf` | Horizon Loader VM Instance | Horizon Loader |
| `toolInstanceOf` | Meridian Collector VM Instance | Meridian Collector |
| `deployedTo` | Horizon Loader VM Instance | Research Document VM |
| `deployedTo` | Meridian Collector VM Instance | Research Document VM |

## Modelling Considerations

The scenario highlights several aspects of the metamodel:

- **Organizational context:** `operatesIn`, `basedIn`, and `countryPartOf` describe the institute's sector, location, and international context.
- **Campaign targeting:** `focusesOnCountry`, `targetsInternationalBody`, and `targetsSector` connect the campaign to the geographic, institutional, and sectoral dimensions of the victim's context.
- **Threat actor identification:** `aliasOf` connects Ghost Meridian to Silent Horizon Group. Only the primary actor identity is directly linked to the threat through `initiates`.
- **Virtualized infrastructure:** `madeBy` connects both nodes to the infrastructure, while `runs` represents the hosting dependency between the physical hypervisor and the research document VM.
- **Application representation:** `runsApp`, `applicationInstanceOf`, and `applicationImplementsCode` distinguish the running portal instance, its application definition, and the document viewer code.
- **Legitimate user access:** `hasAccessTo`, `launches`, and `userAccessesInformation` represent the researcher's access to the VM, use of the viewer, and access to confidential results. `accessesInformation` models the access performed by the code itself.
- **Threat representation and attack sequence:** `threatPartOf`, `startsWith`, and `followedBy` connect the threat to the campaign and describe its two ordered attack steps.
- **Vulnerability exploitation:** `exploits` connects the initial compromise step to a directly instantiated generic `Vulnerability`.
- **Multistage attack tools:** `employsTool` identifies the instance used in each step; `deploysTool` represents the loader deploying the collector; `toolInstanceOf` connects each instance to its tool definition; and `deployedTo` connects both instances to the research document VM.

### Vulnerability Representation

The generic `Vulnerability` class is instantiated directly rather than through `SoftwareVulnerability`, `ConfigVulnerability`, or `HumanVulnerability`. The fictional weakness uses the identifier **ARI-VULN-001** and has severity High. Its `cvss_score` is explicitly `None` in Python and `null` in YAML because the scenario provides insufficient technical evidence for a CVSS assessment.

The relationship `exploits` identifies the weakness associated with the initial attack step. No specific affected software or configuration relationship is introduced for the unclassified vulnerability.

### Information Collection Representation

The researcher account and its access relationships describe legitimate infrastructure usage. The abuse of an accessible research session and the collection of confidential information are represented through the descriptions, objectives, preconditions, and postconditions of the attack steps. No direct `ThreatStep`-to-`Information` relationship is introduced, as this is not defined by the metamodel.

## Contents

| Path | Purpose |
|---|---|
| `scenario.yaml` | Structured representation of the scenario, including entities, attributes, and relationships. |
| `implementation.py` | Python implementation using the CTI Feasibility Metamodel package. |
| `data/` | Supporting input files, such as CTI datasets, JSON files, or STIX bundles. |
| `diagrams/` | Visual representation of the instantiated entities, relationships, and attack sequence. |
| `output/` | Generated reports, validation results, or graph exports. |
| `notes/` | Modelling assumptions, design decisions, and observations. |

## Run

From the repository root:

```bash
python case_studies/05_case_study/implementation.py
```

The script builds the model, performs validation, and prints the number of instantiated entities and relationships.

Expected output:

```text
Case Study 5
Entities: 23
Relationships: 31
Valid: True
```

## Validation

The Python implementation and YAML representation have both been executed and validated successfully.

The model contains:

- **23 entities:** 4 Organization entities, 8 Infrastructure entities, and 11 CyberThreat entities.
- **31 relationships:** 3 Organization relationships, 12 Infrastructure relationships, and 16 CyberThreat relationships.
- **18 distinct entity types** and **27 distinct relationship types**.
- **Validation result:** `True`, with no reported errors or warnings.

The entities reconstructed from `scenario.yaml` have the same classes, names, descriptions, and domain attributes as those created by `implementation.py`. Relationship types, source entities, and target entities also match. Runtime UUIDs differ naturally because each model is instantiated independently.

The model satisfies the formal validation rules currently implemented in the CTI Feasibility Metamodel, with the revised cardinalities of `runs` and `initiates`. This result confirms structural consistency under those rules; it does not by itself establish that a real-world cyberattack would be feasible.

## Status

**Completed and validated.**

The case study provides a validated example of coordinated cyber-espionage, showing how actor aliases, campaign targeting, virtualized infrastructure, user access, generic vulnerabilities, and multistage attack tools can be modelled together in a single scenario. The Python implementation and YAML representation have both been executed and validated successfully.
