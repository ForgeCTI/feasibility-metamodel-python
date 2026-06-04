from metamodel.core.ValidationReport import ValidationReport


def validateTypes(model) -> ValidationReport:
    report = ValidationReport()
    for rel in model.relationships:
        if rel.source_type is not None and not isinstance(rel.source_entity, rel.source_type):
            report.add_error("typeValidator", f"{rel.type} has invalid source type {rel.source_entity.type}.")
        if rel.target_type is not None and not isinstance(rel.target_entity, rel.target_type):
            report.add_error("typeValidator", f"{rel.type} has invalid target type {rel.target_entity.type}.")
    return report
