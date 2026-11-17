# Case studies

This folder contains five synthetic case studies developed with the CTI Feasibility Metamodel. Unlike the [`examples/`](../examples/) folder, which contains small didactic demonstrations, these case studies provide larger, scenario-specific models that combine entities and relationships from one or more of the **Organization**, **Infrastructure**, and **CyberThreat** submodels.

The objectives are to exercise all registered domain entity and relationship types across the five scenarios, verify formal model consistency, and provide corresponding Python, YAML and graphical representations. The first two scenarios focus on organizational and infrastructure modelling; the remaining three introduce cyber-threat modelling.

## Case studies overview

| Case study | Description | Entities | Relationships | Status |
|---|---|---:|---:|---|
| [01 – Healthcare Organization IT Infrastructure](./01_case_study/) | Healthcare appointment booking infrastructure, application deployment, network service and administrative user. | 13 | 12 | Completed |
| [02 – Logistics Tracking Infrastructure](./02_case_study/) | Multi-server shipment tracking infrastructure, network connections, resource hosting and information access. | 17 | 18 | Completed |
| [03 – Credential Phishing Campaign](./03_case_study/) | Credential phishing, human vulnerability, attack steps and threat intelligence. | 20 | 23 | Completed |
| [04 – Exploitation of a Vulnerable Enterprise System](./04_case_study/) | Software and configuration vulnerabilities, enterprise assets and security requirements. | 25 | 38 | Completed |
| [05 – Coordinated Cyber-Espionage Campaign](./05_case_study/) | Threat actor aliases, virtualized infrastructure, legitimate user access and multistage tool deployment. | 23 | 31 | Completed |
| **Total** | | **98** | **122** | |

The counts above refer to entity and relationship instances, not distinct metamodel types. All scenarios use synthetic incident and system data.

## Metamodel coverage

Coverage is calculated by comparing the union of the explicit types used in the five `scenario.yaml` files with the domain types registered in [`registry_data.py`](../src/metamodel/registry_data.py). Each type is counted only once. Inherited entity types are counted only when instantiated directly; inheritance itself is not counted as a relationship instance.

### Coverage by submodel

| Submodel | Entity types covered | Relationship types covered |
|---|---:|---:|
| Organization | 8/8 (100%) | 7/7 (100%) |
| Infrastructure | 15/15 (100%) | 24/24 (100%) |
| CyberThreat | 16/16 (100%) | 31/31 (100%) |
| **Total** | **39/39 (100%)** | **62/62 (100%)** |

Cross-submodel relationships are assigned to the submodel in which their classes are defined. The reference is the revised registry, in which `softwareVulnerabilityIsA` has been removed in favour of class inheritance.

### Cumulative coverage

| Case studies included | New entity types | Cumulative entity coverage | New relationship types | Cumulative relationship coverage |
|---|---:|---:|---:|---:|
| 01 | 13 | 13/39 (33.3%) | 12 | 12/62 (19.4%) |
| 01–02 | 6 | 19/39 (48.7%) | 10 | 22/62 (35.5%) |
| 01–03 | 13 | 32/39 (82.1%) | 18 | 40/62 (64.5%) |
| 01–04 | 6 | 38/39 (97.4%) | 14 | 54/62 (87.1%) |
| **01–05** | **1** | **39/39 (100.0%)** | **8** | **62/62 (100.0%)** |

### Coverage matrix

A check mark (`✓`) indicates that the corresponding type is explicitly instantiated at least once in the scenario. A dash (`—`) indicates that the type is not used. CS01–CS05 refer to the five case studies listed above. Expand each section to inspect all 101 registered types.

<details>
<summary>Organization — entity types (8)</summary>

| Type | CS01 | CS02 | CS03 | CS04 | CS05 |
|---|:---:|:---:|:---:|:---:|:---:|
| `Asset` | — | — | — | ✓ | — |
| `AssetSecurityRequirement` | — | — | — | ✓ | — |
| `BusinessRequirement` | — | — | — | ✓ | — |
| `HomeCountry` | ✓ | — | — | — | ✓ |
| `InternationalBody` | ✓ | — | — | — | ✓ |
| `Organization` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `Sector` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `SecurityRequirement` | — | — | — | ✓ | — |

</details>

<details>
<summary>Infrastructure — entity types (15)</summary>

| Type | CS01 | CS02 | CS03 | CS04 | CS05 |
|---|:---:|:---:|:---:|:---:|:---:|
| `Application` | ✓ | ✓ | — | ✓ | ✓ |
| `ApplicationInstance` | ✓ | ✓ | — | ✓ | ✓ |
| `Code` | — | ✓ | — | ✓ | ✓ |
| `Connection` | — | ✓ | — | — | — |
| `Information` | — | ✓ | — | — | ✓ |
| `InformationType` | — | ✓ | — | — | — |
| `Infrastructure` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `Node` | ✓ | ✓ | — | ✓ | ✓ |
| `NodeType` | — | ✓ | — | — | — |
| `OS` | ✓ | — | — | ✓ | — |
| `OSInstance` | ✓ | — | — | ✓ | — |
| `Port` | ✓ | ✓ | — | — | — |
| `Resource` | — | ✓ | — | ✓ | — |
| `User` | ✓ | — | ✓ | — | ✓ |
| `UserType` | ✓ | — | ✓ | — | — |

</details>

<details>
<summary>CyberThreat — entity types (16)</summary>

| Type | CS01 | CS02 | CS03 | CS04 | CS05 |
|---|:---:|:---:|:---:|:---:|:---:|
| `Adversary` | — | — | ✓ | — | — |
| `AdversaryType` | — | — | ✓ | — | — |
| `AttackTool` | — | — | ✓ | ✓ | ✓ |
| `AttackToolConfiguration` | — | — | ✓ | ✓ | — |
| `AttackToolInstance` | — | — | ✓ | ✓ | ✓ |
| `Campaign` | — | — | ✓ | — | ✓ |
| `ConfigVulnerability` | — | — | — | ✓ | — |
| `Expertise` | — | — | ✓ | — | — |
| `HumanVulnerability` | — | — | ✓ | — | — |
| `Indicator` | — | — | ✓ | — | — |
| `SoftwareVulnerability` | — | — | — | ✓ | — |
| `TTP` | — | — | ✓ | ✓ | — |
| `Threat` | — | — | ✓ | ✓ | ✓ |
| `ThreatActor` | — | — | ✓ | ✓ | ✓ |
| `ThreatStep` | — | — | ✓ | ✓ | ✓ |
| `Vulnerability` | — | — | — | — | ✓ |

</details>

<details>
<summary>Organization — relationship types (7)</summary>

| Type | CS01 | CS02 | CS03 | CS04 | CS05 |
|---|:---:|:---:|:---:|:---:|:---:|
| `basedIn` | ✓ | — | — | — | ✓ |
| `countryPartOf` | ✓ | — | — | — | ✓ |
| `drivesSecurityRequirement` | — | — | — | ✓ | — |
| `hasBusinessRequirement` | — | — | — | ✓ | — |
| `hasSecurityRequirement` | — | — | — | ✓ | — |
| `implementsRequirement` | — | — | — | ✓ | — |
| `operatesIn` | ✓ | ✓ | ✓ | ✓ | ✓ |

</details>

<details>
<summary>Infrastructure — relationship types (24)</summary>

| Type | CS01 | CS02 | CS03 | CS04 | CS05 |
|---|:---:|:---:|:---:|:---:|:---:|
| `accessesInformation` | — | ✓ | — | — | ✓ |
| `applicationImplementsCode` | — | ✓ | — | ✓ | ✓ |
| `applicationInstanceOf` | ✓ | ✓ | — | ✓ | ✓ |
| `exposesPort` | ✓ | — | — | — | — |
| `hasAccessTo` | — | — | — | — | ✓ |
| `hasDestinationPort` | — | ✓ | — | — | — |
| `hasInformationType` | — | ✓ | — | — | — |
| `hasNodeType` | — | ✓ | — | — | — |
| `hasUserType` | ✓ | — | ✓ | — | — |
| `hostsResource` | — | ✓ | — | ✓ | — |
| `isDestination` | — | ✓ | — | — | — |
| `isSource` | — | ✓ | — | — | — |
| `launches` | — | — | — | — | ✓ |
| `listensOn` | — | ✓ | — | — | — |
| `madeBy` | ✓ | ✓ | — | ✓ | ✓ |
| `manages` | ✓ | ✓ | ✓ | ✓ | ✓ |
| `osInstanceOf` | ✓ | — | — | ✓ | — |
| `resourceImplementsAsset` | — | — | — | ✓ | — |
| `resourceImplementsCode` | — | ✓ | — | — | — |
| `runs` | — | — | — | — | ✓ |
| `runsApp` | ✓ | ✓ | — | ✓ | ✓ |
| `runsOS` | ✓ | — | — | ✓ | — |
| `usedBy` | ✓ | — | ✓ | — | ✓ |
| `userAccessesInformation` | — | — | — | — | ✓ |

</details>

<details>
<summary>CyberThreat — relationship types (31)</summary>

| Type | CS01 | CS02 | CS03 | CS04 | CS05 |
|---|:---:|:---:|:---:|:---:|:---:|
| `affectsApplication` | — | — | — | ✓ | — |
| `affectsCode` | — | — | — | ✓ | — |
| `affectsOS` | — | — | — | ✓ | — |
| `affectsUser` | — | — | ✓ | — | — |
| `aliasOf` | — | — | — | — | ✓ |
| `associatedToTool` | — | — | ✓ | — | — |
| `compromises` | — | — | — | ✓ | — |
| `deployedTo` | — | — | — | ✓ | ✓ |
| `deploysTool` | — | — | — | — | ✓ |
| `designedFor` | — | — | — | ✓ | — |
| `employsTool` | — | — | ✓ | ✓ | ✓ |
| `exploits` | — | — | ✓ | ✓ | ✓ |
| `exploitsVulnerability` | — | — | — | ✓ | — |
| `focusesOnCountry` | — | — | — | — | ✓ |
| `followedBy` | — | — | ✓ | ✓ | ✓ |
| `hasAdversaryType` | — | — | ✓ | — | — |
| `hasConfig` | — | — | ✓ | ✓ | — |
| `hasExpertise` | — | — | ✓ | — | — |
| `implementsTTP` | — | — | ✓ | ✓ | — |
| `initiates` | — | — | ✓ | ✓ | ✓ |
| `producesIndicator` | — | — | ✓ | — | — |
| `relatedTo` | — | — | ✓ | — | — |
| `requiresConfig` | — | — | ✓ | ✓ | — |
| `requiresExpertise` | — | — | ✓ | — | — |
| `startsWith` | — | — | ✓ | ✓ | ✓ |
| `targetsInternationalBody` | — | — | — | — | ✓ |
| `targetsResource` | — | — | — | ✓ | — |
| `targetsSector` | — | — | ✓ | — | ✓ |
| `threatPartOf` | — | — | ✓ | — | ✓ |
| `toolInstanceOf` | — | — | ✓ | ✓ | ✓ |
| `violates` | — | — | — | ✓ | — |

</details>

## Folder structure

Each case study follows the same folder convention:

```text
case_studies/
├── README.md
├── 01_case_study/
├── 02_case_study/
├── 03_case_study/
├── 04_case_study/
└── 05_case_study/
    ├── README.md
    ├── implementation.py
    ├── scenario.yaml
    ├── diagrams/
    │   ├── 05_case_study.drawio
    │   └── 05_case_study.svg
    ├── data/
    ├── output/
    └── notes/
```

The fifth case study is shown as an example; diagram filenames follow the case study number.

| File or directory | Purpose |
|---|---|
| `README.md` | Scenario description, model contents and validation results. |
| `implementation.py` | Programmatic instantiation using the metamodel classes. |
| `scenario.yaml` | Declarative scenario representation. |
| `diagrams/` | Editable Draw.io diagrams and SVG exports. |
| `data/` | Optional supporting data. |
| `output/` | Optional generated reports and exports. |
| `notes/` | Optional assumptions and modelling notes. |

## Execution and validation

From the repository root, with the package installed and YAML support available, run a case study using the following command:

```bash
python case_studies/05_case_study/implementation.py
```

Expected output:

```text
Case Study 5
Entities: 23
Relationships: 31
Valid: True
```

To validate its declarative counterpart:

```bash
metamodel validate case_studies/05_case_study/scenario.yaml
```

The validation command exits with code `0` on success and `1` if the model is invalid. With no errors or warnings, it may produce no console output. Replace `05_case_study` with the desired case study directory to run the other scenarios.

### Validation results

| Case study | Python model valid | YAML model valid | Errors (Python / YAML) | Warnings (Python / YAML) |
|---|:---:|:---:|:---:|:---:|
| 01 | `True` | `True` | 0 / 0 | 0 / 0 |
| 02 | `True` | `True` | 0 / 0 | 0 / 0 |
| 03 | `True` | `True` | 0 / 0 | 0 / 0 |
| 04 | `True` | `True` | 0 / 0 | 0 / 0 |
| 05 | `True` | `True` | 0 / 0 | 0 / 0 |

**Scope of the results.** Complete type coverage and successful formal validation demonstrate coverage of the registered domain vocabulary and consistency with the implemented validation rules. They do not establish real-world attack feasibility or exhaustive coverage of all possible instance combinations, cardinality boundaries or semantic constraints.
