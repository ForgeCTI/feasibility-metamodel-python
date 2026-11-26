from metamodel.core.ValidationReport import ValidationReport


def validateTypes(model) -> ValidationReport:
    """Validate relationship endpoint types.

    Check that each endpoint is compatible with the type declared
    by its relationship class, supporting entity inheritance.

    Report undefined endpoint types and incompatible endpoint
    instances as validation errors.
    """

    report = ValidationReport()

    for rel in model.relationships:
        for role, entity, expected_type in (
            ("source", rel.source_entity, rel.source_type),
            ("target", rel.target_entity, rel.target_type),
        ):
            if expected_type is None:
                report.add_error(
                    "typeValidator",
                    f"{rel.type} has undefined {role}_type.",
                )
            elif not isinstance(entity, expected_type):
                report.add_error(
                    "typeValidator",
                    f"{rel.type} has invalid {role} type {type(entity).__name__}.",
                )

    return report