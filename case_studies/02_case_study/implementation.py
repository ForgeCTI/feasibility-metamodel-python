"""
Case Study 02 - Logistics Tracking Infrastructure.

This case study models the IT infrastructure of a fictional
logistics company, "Northstar Logistics".

The scenario focuses on a shipment tracking system composed
of interconnected servers, applications, resources, and data.

The purpose is to demonstrate more complex relationships
within the Organization and Infrastructure submodels.
"""

from metamodel.core.Model import Model

# Organization entities
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector

# Infrastructure entities
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.NodeType import NodeType
from metamodel.infrastructure.entities.Connection import Connection
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.infrastructure.entities.Information import Information
from metamodel.infrastructure.entities.InformationType import InformationType
from metamodel.infrastructure.entities.Code import Code
from metamodel.infrastructure.entities.Application import Application
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.Port import Port

# Organization relationships
from metamodel.organization.rels.operatesIn import operatesIn

# Infrastructure relationships
from metamodel.infrastructure.rels.manages import manages
from metamodel.infrastructure.rels.madeBy import madeBy
from metamodel.infrastructure.rels.hasNodeType import hasNodeType
from metamodel.infrastructure.rels.isSource import isSource
from metamodel.infrastructure.rels.isDestination import isDestination
from metamodel.infrastructure.rels.hostsResource import hostsResource
from metamodel.infrastructure.rels.hasInformationType import hasInformationType
from metamodel.infrastructure.rels.resourceImplementsCode import resourceImplementsCode
from metamodel.infrastructure.rels.accessesInformation import accessesInformation
from metamodel.infrastructure.rels.runsApp import runsApp
from metamodel.infrastructure.rels.applicationInstanceOf import applicationInstanceOf
from metamodel.infrastructure.rels.applicationImplementsCode import applicationImplementsCode
from metamodel.infrastructure.rels.hasDestinationPort import hasDestinationPort
from metamodel.infrastructure.rels.listensOn import listensOn

def build_model() -> Model:
    """Build the fictional Northstar Logistics infrastructure scenario."""
    model = Model()

    organization = model.add(
        Organization(
            name="Northstar Logistics",
            description="Fictional company providing logistics and shipment services.",
            legal_name="Northstar Logistics S.r.l.",
            short_name="NL",
            website="https://northstar-logistics.example",
            organization_size="Medium",
            criticality="High",
            maturity_level="Intermediate",
            source="Synthetic case study data",
        )
    )

    sector = model.add(
        Sector(
            name="Logistics and Transportation",
            description="Transportation, warehousing, and logistics services.",
            sector_code="52.29",
            sector_standard="NACE",
            sector_standard_version="Rev. 2",
            source="Synthetic case study data",
        )
    )

    infrastructure = model.add(
        Infrastructure(
            name="Northstar Shipment Tracking Infrastructure",
            description="IT infrastructure supporting shipment tracking operations.",
            environment_type="Production",
            scope="Shipment tracking and logistics management",
            source="Synthetic case study data",
        )
    )

    application_server_type = model.add(
        NodeType(
            name="Application Server",
            description=(
                "Server category responsible for executing "
                "the shipment tracking application."
            ),
            category="Server",
            source="Synthetic case study data",
        )
    )

    database_server_type = model.add(
        NodeType(
            name="Database Server",
            description=(
                "Server category responsible for storing "
                "and managing shipment tracking data."
            ),
            category="Server",
            source="Synthetic case study data",
        )
    )

    application_server = model.add(
        Node(
            name="Tracking Application Server",
            description=(
                "Server hosting the shipment tracking "
                "application used by logistics operators."
            ),
            hostname="srv-tracking-app-01",
            ip_addresses=["192.0.2.21"],
            mac_addresses=["02:00:00:00:00:21"],
            fqdn="srv-tracking-app-01.northstar-logistics.example",
            source="Synthetic case study data",
        )
    )

    database_server = model.add(
        Node(
            name="Tracking Database Server",
            description=(
                "Server responsible for storing shipment "
                "records, tracking events, and delivery data."
            ),
            hostname="srv-tracking-db-01",
            ip_addresses=["192.0.2.22"],
            mac_addresses=["02:00:00:00:00:22"],
            fqdn="srv-tracking-db-01.northstar-logistics.example",
            source="Synthetic case study data",
        )
    )

    database_connection = model.add(
        Connection(
            name="Tracking Database Connection",
            description=(
                "Encrypted network connection between the "
                "tracking application server and the database server."
            ),
            protocol="TCP",
            encrypted=True,
            allowed=True,
            source="Synthetic case study data",
        )
    )

    tracking_database = model.add(
        Resource(
            name="Shipment Tracking Database",
            description=(
                "Database resource used to store shipment "
                "records and tracking events."
            ),
            source="Synthetic case study data",
        )
    )

    tracking_application_resource = model.add(
        Resource(
            name="Shipment Tracking Application Files",
            description=(
                "Application deployment files and configuration "
                "resources hosted on the tracking application server."
            ),
            source="Synthetic case study data",
        )
    )

    shipment_information = model.add(
        Information(
            name="Shipment Tracking Records",
            description=(
                "Shipment identifiers, current delivery statuses, "
                "and tracking events stored as JSON documents."
            ),
            format="JSON",
            source="Synthetic case study data",
        )
    )

    shipment_information_type = model.add(
        InformationType(
            name="Shipment Tracking Data",
            description=(
                "Information category describing operational "
                "shipment tracking and delivery data."
            ),
            category="Operational Data",
            source="Synthetic case study data",
        )
    )

    tracking_code = model.add(
        Code(
            name="Shipment Tracking Service Code",
            description=(
                "Python application code responsible for processing "
                "shipment tracking events and retrieving shipment records."
            ),
            language="Python",
            version="1.8.0",
            repository_url=(
                "https://git.northstar-logistics.example/tracking-service"
            ),
            source="Synthetic case study data",
        )
    )

    tracking_application = model.add(
        Application(
            name="Northstar Shipment Tracking Application",
            description=(
                "Software product used to manage shipment "
                "tracking and logistics operations."
            ),
            vendor="Northstar Logistics",
            product="Northstar Tracking Platform",
            version="1.8.0",
            cpe=(
                "cpe:2.3:a:northstar_logistics:"
                "northstar_tracking_platform:1.8.0:*:*:*:*:*:*:*"
            ),
            source="Synthetic case study data",
        )
    )

    tracking_application_instance = model.add(
        ApplicationInstance(
            name="Northstar Tracking Production Instance",
            description=(
                "Production deployment of the shipment "
                "tracking application on the application server."
            ),
            version="1.8.0",
            runtime_state="Running",
            source="Synthetic case study data",
        )
    )

    database_port = model.add(
        Port(
            name="PostgreSQL Database Port",
            description=(
                "TCP port used by the PostgreSQL database "
                "service to receive shipment tracking queries."
            ),
            number=5432,
            protocol="tcp",
            service_name="postgresql",
            state="open",
            source="Synthetic case study data",
        )
    )

    database_service_code = model.add(
        Code(
            name="PostgreSQL Database Service Code",
            description=(
                "PostgreSQL server implementation responsible "
                "for handling database connections and queries."
            ),
            language="C",
            version="16.4",
            repository_url="https://github.com/postgres/postgres",
            source="Synthetic case study data",
        )
    )

    model.add(operatesIn(organization, sector))
    model.add(manages(organization, infrastructure))
    model.add(madeBy(infrastructure, application_server))
    model.add(madeBy(infrastructure, database_server))
    model.add(hasNodeType(application_server, application_server_type))
    model.add(hasNodeType(database_server, database_server_type))
    model.add(isSource(application_server, database_connection))
    model.add(isDestination(database_server, database_connection))
    model.add(hostsResource(database_server, tracking_database))
    model.add(hostsResource(application_server, tracking_application_resource))
    model.add(hasInformationType(shipment_information, shipment_information_type))
    model.add(resourceImplementsCode(tracking_application_resource, tracking_code))
    model.add(accessesInformation(tracking_code, shipment_information))
    model.add(runsApp(application_server, tracking_application_instance))
    model.add(applicationInstanceOf(tracking_application_instance, tracking_application))
    model.add(applicationImplementsCode(tracking_application_instance, tracking_code))
    model.add(hasDestinationPort(database_connection, database_port))
    model.add(listensOn(database_service_code, database_port))

    return model


def main() -> None:
    """Run the case-study implementation."""
    model = build_model()
    report = model.validate()

    print("Case Study 2")
    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")

    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
