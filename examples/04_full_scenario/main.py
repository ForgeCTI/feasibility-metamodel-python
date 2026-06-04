"""Integrated organization, infrastructure, and cyber-threat scenario."""

from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.Asset import Asset
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.organization.rels.hasAssetRequirement import hasAssetRequirement
from metamodel.organization.rels.implementsRequirement import implementsRequirement
from metamodel.infrastructure.entities.Node import Node
from metamodel.infrastructure.entities.Resource import Resource
from metamodel.infrastructure.rels.implementsAsset import implementsAsset
from metamodel.cyberThreat.entities.Threat import Threat
from metamodel.cyberThreat.entities.ThreatStep import ThreatStep
from metamodel.cyberThreat.entities.TTP import TTP
from metamodel.cyberThreat.rels.startsWith import startsWith
from metamodel.cyberThreat.rels.implementsTtp import implementsTtp
from metamodel.cyberThreat.rels.targetsResource import targetsResource
from metamodel.cyberThreat.rels.compromises import compromises


def main() -> None:
    model = Model()

    organization = model.add_entity(Organization(name="ExampleBank", criticality="critical"))
    sector = model.add_entity(Sector(name="Finance", taxonomy_ref="sectors:finance"))
    asset = model.add_entity(Asset(name="Online banking service", criticality="critical"))
    security_requirement = model.add_entity(SecurityRequirement(name="Availability", requirement_type="availability"))
    asset_requirement = model.add_entity(AssetSecurityRequirement(name="Online banking availability", priority="high"))

    node = model.add_entity(Node(name="web-server-01", ip_addresses=["10.0.0.10"], exposure="internet_facing"))
    resource = model.add_entity(Resource(name="Online banking API", resource_type="api", criticality="critical"))

    threat = model.add_entity(Threat(name="DDoS-enabled service disruption", objective="service_disruption"))
    step = model.add_entity(ThreatStep(name="Flood public API", sequence_index=1, phase="impact"))
    ttp = model.add_entity(TTP(name="Network Denial of Service", taxonomy_ref="mitreAttackEnterprise:T1498"))

    model.add_relationship(operatesIn(organization, sector))
    model.add_relationship(hasAssetRequirement(asset, asset_requirement))
    model.add_relationship(implementsRequirement(asset_requirement, security_requirement))
    model.add_relationship(implementsAsset(resource, asset))
    model.add_relationship(startsWith(threat, step))
    model.add_relationship(implementsTtp(step, ttp))
    model.add_relationship(targetsResource(step, resource))
    model.add_relationship(compromises(step, asset_requirement))

    report = model.validate()

    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")


if __name__ == "__main__":
    main()
