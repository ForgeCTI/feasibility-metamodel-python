from metamodel.core.ValidationReport import ValidationReport
from metamodel.taxonomies.TaxonomyRegistry import TaxonomyRegistry


def validateTaxonomies(model, taxonomy_registry: TaxonomyRegistry | None = None) -> ValidationReport:
    report = ValidationReport()
    if taxonomy_registry is None:
        try:
            taxonomy_registry = TaxonomyRegistry.load_default()
        except ImportError:
            report.add_warning("taxonomyValidator", "PyYAML is not installed; taxonomy validation skipped.")
            return report

    for entity in model.entities:
        taxonomy_ref = getattr(entity, "taxonomy_ref", None)
        if taxonomy_ref and not taxonomy_registry.contains(taxonomy_ref):
            report.add_error("taxonomyValidator", f"{entity.type} {entity.name!r} references unknown taxonomy concept {taxonomy_ref!r}.")
    return report
