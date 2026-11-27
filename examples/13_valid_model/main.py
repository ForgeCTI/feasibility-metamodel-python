"""Minimal valid model demonstrating relationship validation."""

from metamodel.core.Model import Model
from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Expertise import Expertise
from metamodel.cyberThreat.rels.hasExpertise import hasExpertise


def main() -> None:
    model = Model()

    actor = model.add(
        ThreatActor(name="Example Threat Actor")
    )
    second_actor = model.add(
        ThreatActor(name="Second Example Threat Actor")
    )
    expertise = model.add(
        Expertise(
            name="Social Engineering",
            domain="Social Engineering",
            level="high",
        )
    )

    model.add(hasExpertise(actor, expertise))
    model.add(hasExpertise(second_actor, expertise))

    report = model.validate()

    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")
    print(f"Errors: {len(report.errors)}")
    print(f"Warnings: {len(report.warnings)}")


if __name__ == "__main__":
    main()
