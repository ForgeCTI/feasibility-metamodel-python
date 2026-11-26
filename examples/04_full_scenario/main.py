"""Integrated organization, infrastructure, and cyber-threat scenario."""

from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.Asset import Asset
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.organization.rels.hasSecurityRequirement import hasSecurityRequirement
from metamodel.organization.rels.implementsRequirement import implementsRequirement
from metamodel.infrastructure.entities.Node import Node
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.rels.startsWith import startsWith
from metamodel.cyberThreat.rels.implementsTTP import implementsTTP
from metamodel.cyberThreat.rels.targetsResource import targetsResource
from metamodel.cyberThreat.rels.compromises import compromises


def main() -> None:
    model = Model()

    organization = model.add(Organization(name="ExampleBank", criticality="critical"))
    sector = model.add(Sector(name="Finance"))
    asset = model.add(Asset(name="Online banking service"))
    security_requirement = model.add(SecurityRequirement(name="Availability", requirement_type="availability"))
    asset_requirement = model.add(AssetSecurityRequirement(name="Online banking availability"))

    node = model.add(Node(name="web-server-01", ip_addresses=["10.0.0.10"]))

    threat = model.add(Threat(name="DDoS-enabled service disruption", objective="service_disruption"))
    step = model.add(ThreatStep(name="Flood public API", phase="impact"))
    ttp = model.add(TTP(name="Network Denial of Service", external_id="T1498"))

    model.add(operatesIn(organization, sector))
    model.add(hasSecurityRequirement(asset, asset_requirement))
    model.add(implementsRequirement(asset_requirement, security_requirement))
    model.add(startsWith(threat, step))
    model.add(implementsTTP(step, ttp))
    model.add(targetsResource(step, asset))  # an Asset is a Resource
    model.add(compromises(step, asset_requirement))

    report = model.validate()

    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")


if __name__ == "__main__":
    main()
