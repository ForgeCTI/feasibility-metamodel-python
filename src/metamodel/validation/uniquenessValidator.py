
from metamodel.core.BaseEntity import BaseEntity
from metamodel.core.ValidationReport import ValidationReport


def validateUniqueness(model) -> ValidationReport:
    """Validate relationship uniqueness in the model.

    Check that relationship identifiers are unique and that
    no two relationships have the same type, source and target.

    Return a ValidationReport containing any detected errors.
    """
    report = ValidationReport()

    seen_ids = set()
    seen_connections = set()

    for rel in model.relationships:
        if rel.id in seen_ids:
            report.add_error(
                "uniquenessValidator",
                f"Duplicate relationship id: {rel.id}.",
            )
            continue

        seen_ids.add(rel.id)

        if not isinstance(rel.source_entity, BaseEntity) or not isinstance(
            rel.target_entity, BaseEntity
        ):
            continue

        connection = (
            rel.type,
            rel.source_entity.id,
            rel.target_entity.id,
        )

        if connection in seen_connections:
            report.add_error(
                "uniquenessValidator",
                f"Duplicate relationship: {rel.type} between "
                f"{rel.source_entity.id} and {rel.target_entity.id}.",
            )
        else:
            seen_connections.add(connection)

    return report
