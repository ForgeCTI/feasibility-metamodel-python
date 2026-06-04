from metamodel.core.ValidationReport import ValidationReport
from metamodel.validation.cardinalityValidator import validateCardinalities
from metamodel.validation.referenceValidator import validateReferences
from metamodel.validation.taxonomyValidator import validateTaxonomies
from metamodel.validation.typeValidator import validateTypes


def validateModel(model, *, validate_taxonomies: bool = True) -> ValidationReport:
    report = ValidationReport()
    for validator in (validateReferences, validateTypes, validateCardinalities):
        report.extend(validator(model))
    if validate_taxonomies:
        report.extend(validateTaxonomies(model))
    return report
