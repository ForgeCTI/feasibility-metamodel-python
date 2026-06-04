"""Minimal organization scenario for the CTI Feasibility Metamodel."""

from metamodel.core.Model import Model
from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.entities.Asset import Asset
from metamodel.organization.entities.SecurityRequirement import SecurityRequirement
from metamodel.organization.entities.AssetSecurityRequirement import AssetSecurityRequirement
from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.organization.rels.hasAssetRequirement import hasAssetRequirement
from metamodel.organization.rels.implementsRequirement import implementsRequirement


def main() -> None:
    model = Model()

    organization = model.add_entity(
        Organization(
            name="ExampleBank",
            legal_name="ExampleBank S.p.A.",
            organization_size="enterprise",
            criticality="critical",
            source="Synthetic example",
        )
    )
    sector = model.add_entity(Sector(name="Finance", taxonomy_ref="sectors:finance"))
    asset = model.add_entity(Asset(name="Online banking platform", criticality="critical"))
    security_requirement = model.add_entity(
        SecurityRequirement(
            name="Availability",
            requirement_type="availability",
            taxonomy_ref="securityRequirements:availability",
        )
    )
    asset_requirement = model.add_entity(
        AssetSecurityRequirement(
            name="Online banking must remain available",
            priority="high",
            status="active",
        )
    )

    model.add_relationship(operatesIn(organization, sector))
    model.add_relationship(hasAssetRequirement(asset, asset_requirement))
    model.add_relationship(implementsRequirement(asset_requirement, security_requirement))

    report = model.validate()

    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")
    if report.errors:
        print(report.errors)


if __name__ == "__main__":
    main()
