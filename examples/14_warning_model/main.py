"""Demonstrate a valid model containing an isolated entity."""

from metamodel.core.Model import Model

from metamodel.cyberThreat.entities.ThreatActor import ThreatActor
from metamodel.cyberThreat.entities.Expertise import Expertise
from metamodel.cyberThreat.entities.Adversary import Adversary
from metamodel.cyberThreat.entities.AdversaryType import AdversaryType
from metamodel.infrastructure.entities.Application import Application

from metamodel.cyberThreat.rels.hasExpertise import hasExpertise
from metamodel.cyberThreat.rels.relatedTo import relatedTo
from metamodel.cyberThreat.rels.hasAdversaryType import hasAdversaryType


def main() -> None:
    model = Model()

    actor = model.add(
        ThreatActor(name="Example Threat Actor")
    )
    expertise = model.add(
        Expertise(
            name="Social Engineering",
            domain="Social Engineering",
            level="high",
        )
    )
    adversary = model.add(
        Adversary(name="Social Engineering Adversary")
    )
    adversary_type = model.add(
        AdversaryType(name="Cybercriminal Group")
    )

    model.add(
        Application(name="Standalone Application")
    )

    model.add(hasExpertise(actor, expertise))
    model.add(relatedTo(actor, adversary))
    model.add(hasAdversaryType(adversary, adversary_type))

    report = model.validate()

    print(f"Entities: {len(model.entities)}")
    print(f"Relationships: {len(model.relationships)}")
    print(f"Valid: {report.is_valid}")
    print(f"Errors: {len(report.errors)}")
    print(f"Warnings: {len(report.warnings)}")

    for warning in report.warnings:
        print(f"Warning [{warning.validator}]: {warning.message}")


if __name__ == "__main__":
    main()
