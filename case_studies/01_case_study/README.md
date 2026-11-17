# Case Study 01 - Healthcare Organization IT Infrastructure

This folder contains Case Study 01 for the CTI Feasibility Metamodel.

## Purpose

This case study models the IT infrastructure of a fictional private healthcare clinic, **Clinica Aurora**.

The scenario focuses on the infrastructure supporting a patient appointment booking system, including its server, operating system, application, network port, and administrative user account.

The main objective is to demonstrate how entities and relationships from the **Organization** and **Infrastructure** submodels can be instantiated and connected to represent a coherent organizational and technical environment.

This introductory case study focuses on infrastructure representation rather than cyber-threat modelling or attack feasibility analysis.

## Scenario

Clinica Aurora is a fictional healthcare organization operating in Italy.

Its IT infrastructure supports an appointment booking application hosted on a server running Ubuntu Server. The application is deployed in a production environment, and the server exposes an HTTPS service through TCP port 443.

An administrative user account is associated with the infrastructure and assigned to a user category representing the clinic's administrative staff.

The organization is also connected to its business sector and geographical context.

All clinic-specific information and infrastructure configurations are synthetic.

## Model Implementation

The implementation includes **13 entities** and **12 relationships**, distributed across two submodels.

### Entities

| Submodel | Entity | Instance |
|---|---|---|
| Organization | Organization | Clinica Aurora |
| Organization | Sector | Healthcare |
| Organization | HomeCountry | Italy |
| Organization | InternationalBody | European Union |
| Infrastructure | Infrastructure | Clinica Aurora IT Infrastructure |
| Infrastructure | Node | Booking Server |
| Infrastructure | OS | Ubuntu Server 24.04 LTS |
| Infrastructure | OSInstance | Booking Server OS Installation |
| Infrastructure | Application | Aurora Booking System |
| Infrastructure | ApplicationInstance | Aurora Booking Production Instance |
| Infrastructure | Port | Booking HTTPS Port |
| Infrastructure | User | Booking Office Operator |
| Infrastructure | UserType | Administrative Staff |

### Relationships

| Relationship | Source | Target |
|---|---|---|
| `operatesIn` | Organization | Sector |
| `basedIn` | Organization | HomeCountry |
| `countryPartOf` | HomeCountry | InternationalBody |
| `manages` | Organization | Infrastructure |
| `madeBy` | Infrastructure | Node |
| `runsOS` | Node | OSInstance |
| `osInstanceOf` | OSInstance | OS |
| `runsApp` | Node | ApplicationInstance |
| `applicationInstanceOf` | ApplicationInstance | Application |
| `exposesPort` | Node | Port |
| `usedBy` | Infrastructure | User |
| `hasUserType` | User | UserType |

## Contents

| Path | Purpose |
|---|---|
| `scenario.yaml` | Structured scenario representation synchronized with the Python implementation. |
| `implementation.py` | Python implementation using the CTI Feasibility Metamodel package. |
| `data/` | Supporting input files, if required. |
| `diagrams/` | Visual representation of the instantiated entities and relationships, including draw.io and image exports. |
| `output/` | Generated reports, validation results, or graph exports, if produced. |
| `notes/` | Modelling assumptions, mapping decisions, and unresolved issues. |

## Run

From the repository root:

```bash
python case_studies/01_case_study/implementation.py
```

The script builds the model, performs validation, and prints the number of instantiated entities and relationships.

Expected output:

```text
Case Study 1
Entities: 13
Relationships: 12
Valid: True
```

## Validation

The Python implementation has been executed successfully.

The model contains:

- **13 entities:** 4 Organization entities and 9 Infrastructure entities.
- **12 relationships:** 3 Organization relationships and 9 Infrastructure relationships.
- **Validation result:** `True`, with no reported errors.

This confirms that the scenario satisfies the validation rules currently implemented in the CTI Feasibility Metamodel.

## Status

**Python implementation: Completed and validated.**

**Diagram: Completed.**

**Scenario YAML: Completed.**

The case study provides a validated introductory example of organizational and infrastructure modelling. More complex scenarios involving cybersecurity threats, vulnerabilities, and feasibility analysis will be addressed in subsequent case studies.