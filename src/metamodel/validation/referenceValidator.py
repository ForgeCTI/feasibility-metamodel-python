from metamodel.core.ValidationReport import ValidationReport


def validateReferences(model) -> ValidationReport:
    report = ValidationReport()
    ids = {entity.id for entity in model.entities}
    for rel in model.relationships:
        if rel.source_entity.id not in ids:
            report.add_error("referenceValidator", f"Relationship {rel.id} has a source entity not present in the model.")
        if rel.target_entity.id not in ids:
            report.add_error("referenceValidator", f"Relationship {rel.id} has a target entity not present in the model.")
    return report
