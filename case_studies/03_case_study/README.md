# Case Study 03 - Credential Phishing Campaign

This folder contains Case Study 03 for the CTI Feasibility Metamodel.

## Purpose

This case study models a fictional credential phishing campaign targeting employees of **Bluehaven Consulting**, a management consulting company.

The scenario focuses on the threat actor, phishing campaign, attack techniques, human vulnerabilities, malicious tools, and the sequence of actions involved in credential theft.

The main objective is to demonstrate how entities and relationships from the **Organization**, **Infrastructure**, and **CyberThreat** submodels can be instantiated and combined to represent a coherent cyberattack scenario.

Unlike the previous case studies, which primarily focused on IT infrastructure, this scenario introduces cyber-threat modelling and the representation of an attack sequence.

## Scenario

Bluehaven Consulting is a fictional company operating in the management consulting sector.

The company is targeted by a credential phishing campaign conducted by a fictional threat actor known as **Invoice Lure Group**.

The attacker attempts to obtain employee credentials by distributing fraudulent emails containing links to a deceptive corporate authentication portal.

The attack consists of two main steps:

1. **Phishing Email Delivery:** a fraudulent business email is delivered to the targeted employee.
2. **Credential Capture:** the employee accesses the deceptive login portal and submits their credentials.

The attack steps are associated with MITRE ATT&CK techniques describing spearphishing links and web portal credential capture.

The scenario also includes an employee account susceptible to social engineering, an adversarial profile, the expertise required to conduct the attack, and a phishing tool with its associated instance and configuration.

A fictional domain indicator represents an observable artifact associated with the phishing infrastructure.

All organizations, accounts, threat actors, malicious tools, and attack activities are fictional and intended for demonstration purposes.

## Model Implementation

The implementation contains **20 entities** and **23 relationships**, distributed across the three submodels.

### Entities

| Submodel | Entity | Instance |
|---|---|---|
| Organization | Organization | Bluehaven Consulting |
| Organization | Sector | Management Consulting |
| Infrastructure | Infrastructure | Bluehaven Corporate IT Infrastructure |
| Infrastructure | User | Bluehaven Consulting Employee |
| Infrastructure | UserType | Consulting Staff |
| CyberThreat | ThreatActor | Invoice Lure Group |
| CyberThreat | Campaign | Consulting Sector Credential Phishing Campaign |
| CyberThreat | Threat | Employee Credential Theft |
| CyberThreat | ThreatStep | Phishing Email Delivery |
| CyberThreat | ThreatStep | Credential Capture |
| CyberThreat | TTP | Spearphishing Link |
| CyberThreat | TTP | Web Portal Capture |
| CyberThreat | HumanVulnerability | Phishing Susceptibility |
| CyberThreat | Adversary | Credential Phishing Adversary |
| CyberThreat | AdversaryType | Financially Motivated Cybercriminal |
| CyberThreat | Expertise | Credential Phishing Expertise |
| CyberThreat | AttackTool | Credential Phishing Web Kit |
| CyberThreat | AttackToolInstance | Bluehaven Fake Login Portal Instance |
| CyberThreat | AttackToolConfiguration | Bluehaven Portal Configuration |
| CyberThreat | Indicator | Fake Bluehaven Login Domain |

### Relationships

| Relationship | Source | Target |
|---|---|---|
| `operatesIn` | Bluehaven Consulting | Management Consulting |
| `targetsSector` | Consulting Sector Credential Phishing Campaign | Management Consulting |
| `initiates` | Invoice Lure Group | Employee Credential Theft |
| `threatPartOf` | Employee Credential Theft | Consulting Sector Credential Phishing Campaign |
| `startsWith` | Employee Credential Theft | Phishing Email Delivery |
| `followedBy` | Phishing Email Delivery | Credential Capture |
| `implementsTTP` | Phishing Email Delivery | Spearphishing Link |
| `implementsTTP` | Credential Capture | Web Portal Capture |
| `manages` | Bluehaven Consulting | Bluehaven Corporate IT Infrastructure |
| `usedBy` | Bluehaven Corporate IT Infrastructure | Bluehaven Consulting Employee |
| `hasUserType` | Bluehaven Consulting Employee | Consulting Staff |
| `affectsUser` | Phishing Susceptibility | Bluehaven Consulting Employee |
| `exploits` | Credential Capture | Phishing Susceptibility |
| `relatedTo` | Invoice Lure Group | Credential Phishing Adversary |
| `hasAdversaryType` | Credential Phishing Adversary | Financially Motivated Cybercriminal |
| `hasExpertise` | Invoice Lure Group | Credential Phishing Expertise |
| `employsTool` | Credential Capture | Bluehaven Fake Login Portal Instance |
| `toolInstanceOf` | Bluehaven Fake Login Portal Instance | Credential Phishing Web Kit |
| `hasConfig` | Bluehaven Fake Login Portal Instance | Bluehaven Portal Configuration |
| `requiresConfig` | Credential Phishing Web Kit | Bluehaven Portal Configuration |
| `requiresExpertise` | Credential Phishing Web Kit | Credential Phishing Expertise |
| `producesIndicator` | Bluehaven Fake Login Portal Instance | Fake Bluehaven Login Domain |
| `associatedToTool` | Fake Bluehaven Login Domain | Bluehaven Fake Login Portal Instance |

## Modelling Considerations

The scenario highlights several aspects of the metamodel:

- **Threat representation:** the threat actor, campaign, and individual threat are modelled as distinct entities.
- **Attack sequence:** the threat is associated with its initial step through `startsWith`, while `followedBy` represents the progression of the attack.
- **Attack techniques:** individual threat steps are associated with MITRE ATT&CK techniques through `implementsTTP`.
- **Human vulnerability:** the employee account is associated with a vulnerability to social engineering through `affectsUser`.
- **Adversary profiling:** the adversarial profile, its classification, and the threat actor's expertise are represented separately.
- **Attack tools:** the phishing tool is distinguished from its specific instance and configuration.
- **Indicators:** a fictional domain indicator is associated with the phishing tool instance.

### Vulnerability Representation

The scenario models phishing susceptibility through `HumanVulnerability`, connected directly to the targeted employee.

In the Python implementation, `HumanVulnerability` inherits from `Vulnerability`. This allows the `Credential Capture` step to be connected to `Phishing Susceptibility` through the `exploits` relationship, whose target type is `Vulnerability`. The `affectsUser` relationship connects the same vulnerability to the targeted employee. No additional generic vulnerability instance is required.

## Contents

| Path | Purpose |
|---|---|
| `scenario.yaml` | Structured representation of the phishing scenario, including entities, attributes, and relationships. |
| `implementation.py` | Python implementation using the CTI Feasibility Metamodel package. |
| `data/` | Supporting input files, such as CTI datasets, JSON files, or STIX bundles. |
| `diagrams/` | Visual representation of the instantiated entities, relationships, and attack sequence. |
| `output/` | Generated reports, validation results, or graph exports. |
| `notes/` | Modelling assumptions, design decisions, and observations. |

## Run

From the repository root:

```bash
python case_studies/03_case_study/implementation.py
```

The script builds the model, performs validation, and prints the number of instantiated entities and relationships.

Expected output:

```text
Case Study 3
Entities: 20
Relationships: 23
Valid: True
```

## Validation

The Python implementation has been executed successfully.

The model contains:

- **20 entities:** 2 Organization entities, 3 Infrastructure entities, and 15 CyberThreat entities.
- **23 relationships:** 1 Organization relationship, 3 Infrastructure relationships, and 19 CyberThreat relationships.
- **Validation result:** `True`, with no reported errors.

During implementation, a cardinality issue was identified in the `startsWith` relationship and resolved by adjusting its cardinality definition.

The resulting implementation satisfies the validation rules currently implemented in the CTI Feasibility Metamodel.

## Status

**Completed and validated.**

The case study provides a validated example of credential phishing campaign modelling, including threat actor characterization, attack sequencing, technique mapping, human vulnerabilities, malicious tools, and indicators of compromise.