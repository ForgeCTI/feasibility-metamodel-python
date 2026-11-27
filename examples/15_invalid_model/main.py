"""Demonstrate reference and type validation errors."""

from metamodel.core.Model import Model

from metamodel.organization.entities.Organization import Organization
from metamodel.organization.entities.Sector import Sector
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Expertise import Expertise

from metamodel.organization.rels.operatesIn import operatesIn
from metamodel.cyberThreat.rels.hasExpertise import hasExpertise


def main() -> None:
    model = Model()

    organization = model.add(
        Organization(name="Example Organization")
    )
    sector = model.add(
        Sector(name="Finance")
    )
    actor = model.add(
        ThreatActor(name="Example Threat Actor")
    )
    expertise = model.add(
        Expertise(name="Social Engineering")
    )

    # Reference error: the target is not part of the model.
    external_sector = Sector(name="External Sector")
    invalid_reference = operatesIn(
        organization, external_sector
    )

    model._relationships.append(invalid_reference)

    # Type error: the target belongs to the model, but it is not an Expertise instance.
    invalid_type = model.add(
        hasExpertise(actor, expertise)
    )

    invalid_type._target_entity = sector

    # Validate the complete model.
    report = model.validate()

    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")
    print(f"Errors: {len(report.errors)}")
    print(f"Warnings: {len(report.warnings)}")

    for error in report.errors:
        print(f"Error [{error.validator}]: {error.message}")


if __name__ == "__main__":
    main()
