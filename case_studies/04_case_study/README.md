# Case Study 04 - Exploitation of a Vulnerable Enterprise System

This folder contains Case Study 04 for the CTI Feasibility Metamodel.

## Purpose

This case study models a fictional intrusion targeting the order-processing environment of **Meridian Industrial Systems**, an industrial components manufacturer.

The scenario focuses on the exploitation of a software vulnerability, the abuse of an insecure maintenance-script configuration, and their impact on an organizational business asset and its security requirements.

The main objective is to demonstrate how entities and relationships from the **Organization**, **Infrastructure**, and **CyberThreat** submodels can be instantiated and combined to represent a coherent cyberattack scenario.

In particular, this case study illustrates the connection between a technical weakness, an attack step, the infrastructure resource being targeted, and the organizational requirement potentially compromised. Unlike a purely technical infrastructure example, it explicitly connects the attack to a business process.

## Scenario

Meridian Industrial Systems is a fictional company that manufactures industrial components and manages customer orders through a corporate web portal.

Its production infrastructure includes an application server, the order management service, a portal application and its running instance, an operating system and its installation, and a Python maintenance script used to update order records.

A fictional financially motivated threat actor, **Foundry Access Group**, targets the order-processing environment. The attack consists of two main steps:

1. **Order Portal Exploitation:** the attacker exploits an input-validation weakness in a shared software runtime used by the corporate portal and operating system, bypassing portal protections and obtaining unauthorized functionality.
2. **Maintenance Script Abuse:** the attacker abuses excessive permissions assigned to the maintenance script to alter order records without authorization, using a deployed post-exploitation utility.

The steps are mapped to MITRE ATT&CK techniques **T1190 (Exploit Public-Facing Application)** and **T1059.006 (Command and Scripting Interpreter: Python)**.

The scenario also includes two vulnerability types: a `SoftwareVulnerability` affecting both the application and operating system, and a `ConfigVulnerability` affecting the maintenance script. The software weakness is fictional and has no assigned CVE. Both specialized entities inherit from the generic `Vulnerability` class.

At the organizational level, the order fulfilment process is represented as an `Asset`. The company has a business requirement for reliable order processing, while the asset is associated with a requirement to preserve the integrity of order records. The attack steps are modelled as compromising this asset-specific protection: the first bypasses protective controls and the second enables unauthorized modification of the records.

All organizations, systems, vulnerabilities, adversaries, tools, and incident details are fictional and intended for demonstration purposes. Example addresses and domains are not operational targets.

## Model Implementation

The implementation contains **25 entities** and **38 relationships**, distributed across the three submodels.

### Entities

| Submodel | Entity | Instance |
|---|---|---|
| Organization | Organization | Meridian Industrial Systems |
| Organization | Sector | Industrial Components Manufacturing |
| Organization | BusinessRequirement | Reliable Industrial Order Processing |
| Organization | Asset | Order Fulfilment Process |
| Organization | AssetSecurityRequirement | Order Records Integrity Control |
| Organization | SecurityRequirement | Integrity of Order Records |
| Infrastructure | Infrastructure | Meridian Order Processing Infrastructure |
| Infrastructure | Node | Order Application Server |
| Infrastructure | Resource | Order Management Service |
| Infrastructure | Application | Meridian Order Portal |
| Infrastructure | ApplicationInstance | Order Portal Production Instance |
| Infrastructure | OS | Meridian Server OS |
| Infrastructure | OSInstance | Order Server OS Installation |
| Infrastructure | Code | Order Maintenance Script |
| CyberThreat | ThreatActor | Foundry Access Group |
| CyberThreat | Threat | Order Portal Compromise |
| CyberThreat | ThreatStep | Order Portal Exploitation |
| CyberThreat | ThreatStep | Maintenance Script Abuse |
| CyberThreat | TTP | Exploit Public-Facing Application |
| CyberThreat | TTP | Command and Scripting Interpreter: Python |
| CyberThreat | SoftwareVulnerability | Shared Runtime Input Validation Weakness |
| CyberThreat | ConfigVulnerability | Insecure Maintenance Script Permissions |
| CyberThreat | AttackTool | Remote Order Manipulation Utility |
| CyberThreat | AttackToolInstance | Order Server Intrusion Utility Instance |
| CyberThreat | AttackToolConfiguration | Order Intrusion Utility Configuration |

### Relationships

| Relationship | Source | Target |
|---|---|---|
| `operatesIn` | Meridian Industrial Systems | Industrial Components Manufacturing |
| `hasBusinessRequirement` | Meridian Industrial Systems | Reliable Industrial Order Processing |
| `drivesSecurityRequirement` | Reliable Industrial Order Processing | Order Records Integrity Control |
| `hasSecurityRequirement` | Order Fulfilment Process | Order Records Integrity Control |
| `implementsRequirement` | Order Records Integrity Control | Integrity of Order Records |
| `manages` | Meridian Industrial Systems | Meridian Order Processing Infrastructure |
| `madeBy` | Meridian Order Processing Infrastructure | Order Application Server |
| `hostsResource` | Order Application Server | Order Management Service |
| `runsOS` | Order Application Server | Order Server OS Installation |
| `osInstanceOf` | Order Server OS Installation | Meridian Server OS |
| `runsApp` | Order Application Server | Order Portal Production Instance |
| `applicationInstanceOf` | Order Portal Production Instance | Meridian Order Portal |
| `applicationImplementsCode` | Order Portal Production Instance | Order Maintenance Script |
| `resourceImplementsAsset` | Order Management Service | Order Fulfilment Process |
| `initiates` | Foundry Access Group | Order Portal Compromise |
| `startsWith` | Order Portal Compromise | Order Portal Exploitation |
| `followedBy` | Order Portal Exploitation | Maintenance Script Abuse |
| `implementsTTP` | Order Portal Exploitation | Exploit Public-Facing Application |
| `implementsTTP` | Maintenance Script Abuse | Command and Scripting Interpreter: Python |
| `exploits` | Order Portal Exploitation | Shared Runtime Input Validation Weakness |
| `exploits` | Maintenance Script Abuse | Insecure Maintenance Script Permissions |
| `exploitsVulnerability` | Exploit Public-Facing Application | Shared Runtime Input Validation Weakness |
| `exploitsVulnerability` | Command and Scripting Interpreter: Python | Insecure Maintenance Script Permissions |
| `affectsApplication` | Shared Runtime Input Validation Weakness | Meridian Order Portal |
| `affectsOS` | Shared Runtime Input Validation Weakness | Meridian Server OS |
| `affectsCode` | Insecure Maintenance Script Permissions | Order Maintenance Script |
| `compromises` | Order Portal Exploitation | Order Records Integrity Control |
| `compromises` | Maintenance Script Abuse | Order Records Integrity Control |
| `targetsResource` | Order Portal Exploitation | Order Management Service |
| `targetsResource` | Maintenance Script Abuse | Order Management Service |
| `violates` | Exploit Public-Facing Application | Integrity of Order Records |
| `violates` | Command and Scripting Interpreter: Python | Integrity of Order Records |
| `designedFor` | Order Server Intrusion Utility Instance | Order Server OS Installation |
| `deployedTo` | Order Server Intrusion Utility Instance | Order Application Server |
| `employsTool` | Maintenance Script Abuse | Order Server Intrusion Utility Instance |
| `toolInstanceOf` | Order Server Intrusion Utility Instance | Remote Order Manipulation Utility |
| `hasConfig` | Order Server Intrusion Utility Instance | Order Intrusion Utility Configuration |
| `requiresConfig` | Remote Order Manipulation Utility | Order Intrusion Utility Configuration |

## Modelling Considerations

The scenario highlights several aspects of the metamodel:

- **Business requirements and assets:** `hasBusinessRequirement`, `drivesSecurityRequirement`, `hasSecurityRequirement`, and `implementsRequirement` connect the organization's operational needs to the integrity requirement protecting its order fulfilment process.
- **Infrastructure-to-business mapping:** `resourceImplementsAsset` connects the concrete order management service to the business asset it supports.
- **Threat representation and attack sequence:** `initiates` identifies the threat actor; `startsWith` and `followedBy` represent the two ordered attack steps.
- **Attack techniques:** each `ThreatStep` is linked to a MITRE ATT&CK technique through `implementsTTP`.
- **Vulnerability exploitation:** `exploits` associates a specific attack step with a vulnerability, whereas `exploitsVulnerability` associates a technique (`TTP`) with a vulnerability it can exploit.
- **Technical exposure:** `affectsApplication` and `affectsOS` connect the shared-runtime weakness to the affected software products, while `affectsCode` connects the configuration weakness to the maintenance script.
- **Target and impact:** `targetsResource` identifies the infrastructure service targeted by each step; `compromises` links the steps to the asset-specific requirement; and `violates` links the associated techniques to the generic security requirement.
- **Attack tools:** `AttackTool`, `AttackToolInstance`, and `AttackToolConfiguration` are distinct entities. The tool instance is linked to the target operating-system installation through `designedFor` and to the server through `deployedTo`.

### Vulnerability Representation

`SoftwareVulnerability` and `ConfigVulnerability` inherit from `Vulnerability` in the Python implementation. The inherited `external_id`, `severity`, and `cvss_score` attributes are populated alongside each subclass's domain-specific attributes.

Both vulnerabilities can therefore be used as targets of `exploits` and `exploitsVulnerability`, whose declared target type is `Vulnerability`. No additional generic vulnerability instance is needed for this case study.

The fictional software vulnerability uses `external_id` **MIS-SW-001** and `cwe_id` **CWE-20**. Its `cve_id` is explicitly `None` because no official CVE is assigned to this invented weakness. The configuration vulnerability uses `external_id` **MIS-CFG-001**. Both have a stated severity and a CVSS-like score for the simulated scenario.

The same software vulnerability affects both the portal application and the operating system because the scenario assumes that both depend on a shared vulnerable runtime component. This is a deliberate modelling assumption, not an assertion about a real product.

### Security Requirement Representation

The modelling distinguishes a **business need** (`BusinessRequirement`), a **business asset** (`Asset`), a **security requirement specific to that asset** (`AssetSecurityRequirement`), and a **generic security objective** (`SecurityRequirement`).

Both attack steps are linked to `Order Records Integrity Control` through `compromises`. The first step is interpreted as bypassing the integrity protections of the portal, while the second represents the subsequent unauthorized modification of order data. This distinction makes both relationships meaningful within the fictional scenario and consistent with the declared cardinalities.

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
python case_studies/04_case_study/implementation.py
```

The script builds the model, performs validation, and prints the number of instantiated entities and relationships.

Expected output:

```text
Case Study 4
Entities: 25
Relationships: 38
Valid: True
```

## Validation

The Python implementation and YAML representation have both been executed and validated successfully.

The model contains:

- **25 entities:** 6 Organization entities, 8 Infrastructure entities, and 11 CyberThreat entities.
- **38 relationships:** 5 Organization relationships, 9 Infrastructure relationships, and 24 CyberThreat relationships.
- **Validation result:** `True`, with no reported errors or warnings.

The entities reconstructed from `scenario.yaml` have the same classes, names, descriptions, and domain attributes as those created by `implementation.py`. Relationship types, source entities, and target entities also match. Runtime UUIDs differ naturally because each model is instantiated independently.

The model satisfies the formal validation rules currently implemented in the CTI Feasibility Metamodel. This result confirms structural consistency under those rules; it does not by itself establish that a real-world cyberattack would be feasible.

## Status

**Completed and validated.**

The case study provides a validated example of software and configuration vulnerability exploitation, showing how attack steps, infrastructure components, business assets, and security requirements can be modelled together in a coherent enterprise intrusion scenario.
