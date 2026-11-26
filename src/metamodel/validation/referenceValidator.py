from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationReport import ValidationReport


def validateReferences(model) -> ValidationReport:
    """Validate the referential integrity of the model.

    Check that both endpoints of each relationship reference
    entities present in the model, using their unique identifiers.

    Return a ValidationReport containing any detected violations.
    """

    report = ValidationReport()
    ids = {entity.id for entity in model.entities}

    for rel in model.relationships:
        for role, entity in (("source", rel.source_entity), ("target", rel.target_entity)):
            if not isinstance(entity, BaseEntity):
                continue

            if entity.id not in ids:
                report.add_error(
                    "referenceValidator",
                    f"Relationship {rel.id} has a {role} entity not present in the model.",
                )

        for referenced in rel.referenced_entities():
            if referenced.id not in ids:
                report.add_error(
                    "referenceValidator",
                    f"Relationship {rel.id} references entity {referenced.name!r} not present in the model.",
                )

    return report
