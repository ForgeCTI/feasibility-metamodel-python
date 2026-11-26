# Case Study 02 - Logistics Tracking Infrastructure

This folder contains Case Study 02 for the CTI Feasibility Metamodel.

## Purpose

This case study models the IT infrastructure of a fictional logistics company, **Northstar Logistics**.

The scenario focuses on a shipment tracking system composed of interconnected servers, a tracking application, software components, network connections, and operational data.

The main objective is to demonstrate more complex entity and relationship interactions within the **Organization** and **Infrastructure** submodels, extending the infrastructure modelling concepts introduced in Case Study 01.

This case study focuses on infrastructure modelling and data access rather than cyber-threat modelling or attack feasibility analysis.

## Scenario

Northstar Logistics is a fictional company operating in the logistics and transportation sector.

Its shipment tracking infrastructure consists of two servers:

- **Tracking Application Server:** hosts the shipment tracking application and its deployment resources.
- **Tracking Database Server:** hosts the database resource used to store shipment-related data.

The servers communicate through an encrypted TCP connection, using PostgreSQL port 5432 as the destination port.

The tracking application is implemented using Python code responsible for processing tracking events and accessing shipment information. A separate code entity represents the PostgreSQL database service.

The scenario also distinguishes software products from their deployed instances, technical resources from information, and infrastructure nodes from their functional categories.

All company-specific details and infrastructure configurations are synthetic.

## Model Implementation

The implementation contains **17 entities** and **18 relationships**, distributed across the Organization and Infrastructure submodels.

### Entities

| Submodel | Entity | Instance |
|---|---|---|
| Organization | Organization | Northstar Logistics |
| Organization | Sector | Logistics and Transportation |
| Infrastructure | Infrastructure | Northstar Shipment Tracking Infrastructure |
| Infrastructure | NodeType | Application Server |
| Infrastructure | NodeType | Database Server |
| Infrastructure | Node | Tracking Application Server |
| Infrastructure | Node | Tracking Database Server |
| Infrastructure | Connection | Tracking Database Connection |
| Infrastructure | Resource | Shipment Tracking Database |
| Infrastructure | Resource | Shipment Tracking Application Files |
| Infrastructure | Information | Shipment Tracking Records |
| Infrastructure | InformationType | Shipment Tracking Data |
| Infrastructure | Code | Shipment Tracking Service Code |
| Infrastructure | Application | Northstar Shipment Tracking Application |
| Infrastructure | ApplicationInstance | Northstar Tracking Production Instance |
| Infrastructure | Port | PostgreSQL Database Port |
| Infrastructure | Code | PostgreSQL Database Service Code |

### Relationships

| Relationship | Source | Target |
|---|---|---|
| `operatesIn` | Northstar Logistics | Logistics and Transportation |
| `manages` | Northstar Logistics | Northstar Shipment Tracking Infrastructure |
| `madeBy` | Northstar Shipment Tracking Infrastructure | Tracking Application Server |
| `madeBy` | Northstar Shipment Tracking Infrastructure | Tracking Database Server |
| `hasNodeType` | Tracking Application Server | Application Server |
| `hasNodeType` | Tracking Database Server | Database Server |
| `isSource` | Tracking Application Server | Tracking Database Connection |
| `isDestination` | Tracking Database Server | Tracking Database Connection |
| `hostsResource` | Tracking Database Server | Shipment Tracking Database |
| `hostsResource` | Tracking Application Server | Shipment Tracking Application Files |
| `hasInformationType` | Shipment Tracking Records | Shipment Tracking Data |
| `resourceImplementsCode` | Shipment Tracking Application Files | Shipment Tracking Service Code |
| `accessesInformation` | Shipment Tracking Service Code | Shipment Tracking Records |
| `runsApp` | Tracking Application Server | Northstar Tracking Production Instance |
| `applicationInstanceOf` | Northstar Tracking Production Instance | Northstar Shipment Tracking Application |
| `applicationImplementsCode` | Northstar Tracking Production Instance | Shipment Tracking Service Code |
| `hasDestinationPort` | Tracking Database Connection | PostgreSQL Database Port |
| `listensOn` | PostgreSQL Database Service Code | PostgreSQL Database Port |

## Modelling Considerations

The scenario highlights several aspects of the metamodel:

- **Node classification:** two nodes are associated with different node types.
- **Network communication:** source and destination nodes are connected through a dedicated Connection entity.
- **Resource hosting:** each server hosts at least one technical resource.
- **Software representation:** the application product is distinguished from its production instance and implementation code.
- **Information modelling:** tracking records are classified through InformationType and accessed by the tracking service code.
- **Database communication:** the destination port and the code listening on it are represented explicitly.

The model does not establish a direct relationship between the database resource and the shipment information. This distinction reflects the relationships instantiated in the scenario.

## Contents

| Path | Purpose |
|---|---|
| `scenario.yaml` | Structured representation of the case study, including entities, attributes, and relationships. |
| `implementation.py` | Python implementation using the CTI Feasibility Metamodel package. |
| `data/` | Supporting input files, such as JSON, CSV, or external data sources. |
| `diagrams/` | Visual representation of the instantiated entities and relationships. |
| `output/` | Generated reports, validation results, or graph exports. |
| `notes/` | Modelling assumptions, mapping decisions, and observations. |

## Run

From the repository root:

```bash
python case_studies/02_case_study/implementation.py
```

The script builds the model, performs validation, and prints the number of instantiated entities and relationships.

Expected output:

```text
Case Study 2
Entities: 17
Relationships: 18
Valid: True
```

## Validation

The Python implementation has been executed successfully.

The model contains:

- **17 entities:** 2 Organization entities and 15 Infrastructure entities.
- **18 relationships:** 1 Organization relationship and 17 Infrastructure relationships.
- **Validation result:** `True`, with no reported errors.

During implementation, an initial cardinality validation error was encountered for the `hostsResource` relationship. The issue was resolved by modelling an additional application resource hosted on the Tracking Application Server.

The final implementation satisfies the validation rules currently implemented in the CTI Feasibility Metamodel.

## Status

**Completed and validated.**

The case study provides a validated example of a multi-server infrastructure supporting a logistics tracking application, including network communication, resource hosting, software execution, and information access.

More advanced cybersecurity threats, vulnerabilities, and attack scenarios are addressed in subsequent case studies.