from metamodel.core.ValidationReport import ValidationReport
from metamodel.validation.cardinalityValidator import validateCardinalities
from metamodel.validation.referenceValidator import validateReferences
from metamodel.validation.semanticValidator import validateSemantics
from metamodel.validation.typeValidator import validateTypes


def validateModel(model) -> ValidationReport:
    """Validate the model in two stages.

    First, check references and endpoint types.
    Run cardinality and semantic validation only if no structural errors are found.

    Return a ValidationReport containing errors and warnings.
    """
    report = ValidationReport()

    if not model.entities and not model.relationships:
        report.add_warning(
            "modelValidator",
            "Model is empty: no entities or relationships to validate.",
        )

    report.extend(validateReferences(model))
    report.extend(validateTypes(model))

    if report.is_valid:
        report.extend(validateCardinalities(model))
        report.extend(validateSemantics(model))

    return report
