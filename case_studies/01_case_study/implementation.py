"""Case Study 1 implementation.

This script is a placeholder implementation for Case Study 1.
Expand it with the concrete organization, infrastructure, and cyber-threat entities
required by the scenario.
"""

from metamodel.core.Model import Model

from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.organization.rels.operatesIn import operatesIn


def build_model() -> Model:
    """Build and return the case-study model."""
    model = Model()

    organization = model.add_entity(
        Organization(
            name="Example Organization 1",
            description="Placeholder organization for Case Study 1.",
            source="Case Study 1 notes",
        )
    )

    sector = model.add_entity(
        Sector(
            name="Example Sector",
            taxonomy_ref="sectors:example",
        )
    )

    model.add_relationship(
        operatesIn(
            source_entity=organization,
            target_entity=sector,
        )
    )

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
