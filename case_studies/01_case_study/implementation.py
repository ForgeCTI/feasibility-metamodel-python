"""
Case Study 01 - Healthcare Organization IT Infrastructure.

This case study models the IT infrastructure of a fictional
private healthcare clinic, "Clinica Aurora".

The scenario includes the organization, its business sector,
and the infrastructure supporting a patient booking system.
The infrastructure consists of a server, an operating system,
an application, network services, and authorized users.

The purpose is to demonstrate how entities and relationships
from the Organization and Infrastructure submodels can be
instantiated and combined into a coherent scenario.

"""


from metamodel.core.Model import Model

# Organization entities
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.HomeCountry import HomeCountry
from metamodel.organization.entities.InternationalBody import InternationalBody

# Infrastructure entities
from metamodel.infrastructure.entities.Infrastructure import Infrastructure
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.OS import OS
from metamodel.infrastructure.entities.OSInstance import OSInstance
from metamodel.infrastructure.entities.Application import Application
from metamodel.infrastructure.entities.ApplicationInstance import ApplicationInstance
from metamodel.infrastructure.entities.Port import Port
from metamodel.infrastructure.entities.User import User
from metamodel.infrastructure.entities.UserType import UserType

# Organization relationships
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.organization.rels.basedIn import basedIn
from metamodel.organization.rels.countryPartOf import countryPartOf

# Infrastructure relationships
from metamodel.infrastructure.rels.manages import manages
from metamodel.infrastructure.rels.madeBy import madeBy
from metamodel.infrastructure.rels.usedBy import usedBy
from metamodel.infrastructure.rels.hasUserType import hasUserType
from metamodel.infrastructure.rels.runsOS import runsOS
from metamodel.infrastructure.rels.osInstanceOf import osInstanceOf
from metamodel.infrastructure.rels.runsApp import runsApp
from metamodel.infrastructure.rels.applicationInstanceOf import applicationInstanceOf
from metamodel.infrastructure.rels.exposesPort import exposesPort


def build_model() -> Model:
    """Build the fictional Clinica Aurora infrastructure scenario."""
    model = Model()

    organization = model.add(
        Organization(
            name="Clinica Aurora",
            description="Fictional private healthcare clinic.",
            legal_name="Clinica Aurora S.r.l.",
            short_name="CA",
            website="https://clinica-aurora.example",
            organization_size="Medium",
            criticality="High",
            maturity_level="Intermediate",
            source="Synthetic case study data",
        )
    )

    sector = model.add(
        Sector(
            name="Healthcare",
            description="Hospital and healthcare services.",
            sector_code="86.10",
            sector_standard="NACE",
            sector_standard_version="Rev. 2",
            source="Synthetic case study data",
        )
    )

    infrastructure = model.add(
        Infrastructure(
            name="Clinica Aurora IT Infrastructure",
            description="IT infrastructure supporting patient bookings.",
            environment_type="Production",
            scope="Patient appointment booking system",
            source="Synthetic case study data",
        )
    )

    booking_server = model.add(
        Node(
            name="Booking Server",
            description=(
                "Application server hosting the patient appointment booking system."
            ),
            hostname="srv-booking-01",
            ip_addresses=["192.0.2.10"],
            mac_addresses=["02:00:00:00:00:10"],
            fqdn="srv-booking-01.clinica-aurora.example",
            source="Synthetic case study data",
        )
    )

    ubuntu_os = model.add(
        OS(
            name="Ubuntu Server 24.04 LTS",
            description="Operating system product used by the booking server.",
            vendor="Canonical",
            product="Ubuntu Server",
            version="24.04 LTS",
            cpe="cpe:2.3:o:canonical:ubuntu_linux:24.04:*:*:*:*:*:*:*",
            source="Synthetic case study data",
        )
    )

    ubuntu_instance = model.add(
        OSInstance(
            name="Booking Server OS Installation",
            description="Ubuntu Server installation on the booking server.",
            version="24.04 LTS",
            build="6.8.0-45-generic",
            patch_level="October 2026 security update baseline",
            support_status="Supported",
            source="Synthetic case study data",
        )
    )

    booking_app = model.add(
        Application(
            name="Aurora Booking System",
            description=(
                "Web application used to manage patient appointments and clinic reservations."
            ),
            vendor="Aurora Software",
            product="Aurora Booking",
            version="2.4.1",
            cpe=(
                "cpe:2.3:a:aurora_software:aurora_booking:"
                "2.4.1:*:*:*:*:*:*:*"
            ),
            source="Synthetic case study data",
        )
    )

    booking_app_instance = model.add(
        ApplicationInstance(
            name="Aurora Booking Production Instance",
            description=(
                "Production deployment of the booking application on the clinic server."
            ),
            version="2.4.1",
            runtime_state="Running",
            source="Synthetic case study data",
        )
    )

    https_port = model.add(
        Port(
            name="Booking HTTPS Port",
            description=(
                "TCP port used to expose the patient booking web service over HTTPS."
            ),
            number=443,
            protocol="tcp",
            service_name="https",
            state="open",
            source="Synthetic case study data",
        )
    )

    booking_operator = model.add(
        User(
            name="Booking Office Operator",
            description=(
                "Administrative account used to manage patient appointments."
            ),
            username="booking.operator01",
            email="booking.operator@clinica-aurora.example",
            role="Booking office clerk",
            mfa_enabled=True,
            source="Synthetic case study data",
        )
    )

    administrative_user_type = model.add(
        UserType(
            name="Administrative Staff",
            description=(
                "User category for clinic employees managing administrative operations."
            ),
            privilege_level="Standard",
            source="Synthetic case study data",
        )
    )

    italy = model.add(
        HomeCountry(
            name="Italy",
            description="Country where Clinica Aurora is located.",
            iso2_code="IT",
            iso3_code="ITA",
            region="Southern Europe",
            source="Synthetic case study data",
        )
    )

    european_union = model.add(
        InternationalBody(
            name="European Union",
            description=(
                "Supranational organization of which Italy is a member state."
            ),
            acronym="EU",
            source="Synthetic case study data",
        )
    )

    model.add(operatesIn(organization, sector))
    model.add(manages(organization, infrastructure))
    model.add(madeBy(infrastructure, booking_server))
    model.add(runsOS(booking_server, ubuntu_instance))
    model.add(osInstanceOf(ubuntu_instance, ubuntu_os))
    model.add(runsApp(booking_server, booking_app_instance))
    model.add(applicationInstanceOf(booking_app_instance, booking_app))
    model.add(exposesPort(booking_server, https_port))
    model.add(usedBy(infrastructure, booking_operator))
    model.add(hasUserType(booking_operator, administrative_user_type))
    model.add(basedIn(organization, italy))
    model.add(countryPartOf(italy, european_union))

    return model


def main() -> None:
    """Run the case-study implementation."""
    model = build_model()
    report = model.validate()

    print("Case Study 1")
    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")

    if report.errors:
        print("Errors:")
        for error in report.errors:
            print(f"- {error}")


if __name__ == "__main__":
    main()
